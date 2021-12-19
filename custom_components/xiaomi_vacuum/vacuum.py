"""Xiaomi Vacuum"""
from functools import partial
import logging
import voluptuous as vol
import time
import re
from .const import *

from .miio import DreameVacuum, DeviceException


from homeassistant.const import CONF_HOST, CONF_NAME, CONF_TOKEN
from homeassistant.helpers import config_validation as cv, entity_platform

_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_TOKEN): vol.All(str, vol.Length(min=32, max=32)),
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_NO_SLEEP_DOCKED, default=False): cv.boolean,
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Xiaomi vacuum cleaner robot platform."""
    if DATA_KEY not in hass.data:
        hass.data[DATA_KEY] = {}

    host = config.get(CONF_HOST)
    token = config.get(CONF_TOKEN)
    name = config.get(CONF_NAME)
    no_sleep_when_docked = config.get(CONF_NO_SLEEP_DOCKED)

    # Create handler
    _LOGGER.info("Initializing with host %s (token %s...)", host, token[:5])
    vacuum = DreameVacuum(host, token)

    mirobo = MiroboVacuum(name, vacuum, no_sleep_when_docked)
    hass.data[DATA_KEY][host] = mirobo

    async_add_entities([mirobo], update_before_add=True)

    platform = entity_platform.current_platform.get()

    platform.async_register_entity_service(
        SERVICE_FAST_MAP,
        {},
        MiroboVacuum.async_fast_map.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_SELECT_MAP,
        {
            vol.Required(INPUT_MAP_ID): cv.positive_int,
        },
        MiroboVacuum.async_select_map.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_CLEAN_ZONE,
        {
            vol.Required(INPUT_ZONE_ARRAY): cv.string,
            vol.Required(INPUT_ZONE_REPEATER): vol.All(
                vol.Coerce(int), vol.Clamp(min=1, max=10)
            ),
        },
        MiroboVacuum.async_clean_zone.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_CLEAN_ROOM_BY_ID,
        {
            vol.Required(INPUT_ROOMS_ARRAY): cv.ensure_list,
            vol.Required(INPUT_ZONE_REPEATER): vol.All(
                vol.Coerce(int), vol.Clamp(min=1, max=10)
            ),
            vol.Required(INPUT_CLEAN_MODE): vol.All(
                vol.Coerce(int), vol.Clamp(min=0, max=3)
            ),
            vol.Required(INPUT_MOP_MODE): vol.All(
                vol.Coerce(int), vol.Clamp(min=1, max=3)
            ),
        },
        MiroboVacuum.async_clean_room_by_id.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_SET_RESTRICTED_ZONE,
        {
            vol.Optional(INPUT_WALL_ARRAY): cv.string,
            vol.Optional(INPUT_ZONES_ARRAY): cv.string,
            vol.Optional(INPUT_MOP_ARRAY): cv.string,
        },
        MiroboVacuum.async_set_restricted_zone.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_RESET_FILTER_LIFE,
        {},
        MiroboVacuum.async_reset_filter_life.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_RESET_MAIN_BRUSH_LIFE,
        {},
        MiroboVacuum.async_reset_main_brush_life.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_RESET_SIDE_BRUSH_LIFE2,
        {},
        MiroboVacuum.async_reset_side_brush_life.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_MOVE_REMOTE_CONTROL_STEP,
        {
            vol.Required(INPUT_RC_VELOCITY): vol.All(
                vol.Coerce(int), vol.Clamp(min=-300, max=100)
            ),
            vol.Required(INPUT_RC_ROTATION): vol.All(
                vol.Coerce(int), vol.Clamp(min=-128, max=128)
            ),
        },
        MiroboVacuum.async_remote_control_move_step.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_WATER_LEVEL,
        {
            vol.Required(ATTR_WATER_LEVEL): cv.string,
        },
        MiroboVacuum.async_set_water_level.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_SET_AUDIO_VOLUME,
        {
            vol.Required(INPUT_VOLUME): vol.All(
                vol.Coerce(int), vol.Clamp(min=0, max=100)
            ),
        },
        MiroboVacuum.async_set_audio_volume.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_INSTALL_VOICE_PACK,
        {
            vol.Required(INPUT_LANGUAGE_ID): cv.string,
            vol.Required(INPUT_URL): cv.string,
            vol.Required(INPUT_MD5): cv.string,
            vol.Required(INPUT_SIZE): cv.positive_int,
        },
        MiroboVacuum.async_install_voice_pack.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_SET_CLEAN_CLOTH_TIP,
        {
            vol.Required(INPUT_DELAY): vol.Clamp(min=0, max=120),
        },
        MiroboVacuum.async_set_clean_cloth_tip.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_DND,
        {
            vol.Optional(INPUT_DND_ENABLED): cv.boolean,
            vol.Optional(INPUT_DND_START): cv.string,
            vol.Optional(INPUT_DND_STOP): cv.string,
        },
        MiroboVacuum.async_do_not_disturb.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_SET_CARPET_BOOST,
        {
            vol.Required(INPUT_CARPET_BOOST_ENABLED): cv.boolean,
        },
        MiroboVacuum.async_set_carpet_boost.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_SET_MULTI_MAP,
        {
            vol.Required(INPUT_MULTI_MAP_ENABLED): cv.boolean,
        },
        MiroboVacuum.async_multi_map.__name__,
    )

    platform.async_register_entity_service(
        SERVICE_RENAME_MAP,
        {
            vol.Required(INPUT_MAP_ID): cv.string,
            vol.Required(INPUT_MAP_NAME): cv.string,
        },
        MiroboVacuum.async_rename_map.__name__,
    )


class MiroboVacuum(StateVacuumEntity):
    """Representation of a Xiaomi Vacuum cleaner robot."""

    def __init__(self, name, vacuum, no_sleep_when_docked):
        """Initialize the Xiaomi vacuum cleaner robot handler."""
        self._name = name
        self._vacuum: DreameVacuum = vacuum
        self._no_sleep_when_docked = no_sleep_when_docked

        self._fan_speeds = None
        self._fan_speeds_reverse = None

        self.vacuum_last_state = None
        self.vacuum_state = None
        self.vacuum_error = None
        self.battery_percentage = None

        self._current_fan_speed = None

        self._main_brush_time_left = None
        self._main_brush_life_level = None

        self._side_brush_time_left = None
        self._side_brush_life_level = None

        self._filter_life_level = None
        self._filter_left_time = None

        self._total_clean_count = None
        self._total_clean_time = None
        self._total_log_start = None
        self._total_clean_area = None

        self._cleaning_area = None
        self._cleaning_time = None

        self._waterbox_status = None
        self._water_level = None
        self._current_water_level = None
        self._water_level_reverse = None

        self._operation_status = None
        self._operating_mode = None
        self._schedule = ""

        self._carpet_boost = None

        self._dnd_enabled = None
        self._dnd_start_time = None
        self._dnd_stop_time = None

        self._multi_map_enabled = None

        self._audio_volume = None
        self._audio_language = None

        self._timezone = None

        self._clean_cloth_tip = None

        self._serial_number = None

        self.time_pattern = re.compile("([0-1][0-9]|2[0-3]):[0-5][0-9]$")

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the status of the vacuum cleaner."""
        if self.vacuum_state is not None:
            try:
                return STATE_CODE_TO_STATE[self.vacuum_state]
            except KeyError:
                _LOGGER.error("STATE_CODE not supported: %s", self.vacuum_state)
                return None

    @property
    def error(self):
        """Return the error of the vacuum cleaner."""
        if self.vacuum_error is not None:
            try:
                return ERROR_CODE_TO_ERROR.get(self.vacuum_error, "Unknown")
            except KeyError:
                _LOGGER.error("ERROR_CODE not supported: %s", self.vacuum_error)
                return None

    @property
    def battery_level(self):
        """Return the battery level of the vacuum cleaner."""
        return self.battery_percentage

    @property
    def fan_speed(self):
        """Return the fan speed of the vacuum cleaner."""
        if self._current_fan_speed is not None:
            try:
                return SPEED_CODE_TO_NAME.get(self._current_fan_speed, "Unknown")
            except KeyError:
                _LOGGER.error("SPEED_CODE not supported: %s", self._current_fan_speed)
            return None

    @property
    def water_level(self):
        """Return the water level of the vacuum cleaner."""
        if self._current_water_level is not None:
            try:
                return WATER_CODE_TO_NAME.get(self._current_water_level, "Unknown")
            except KeyError:
                _LOGGER.error("WATER_CODE not supported %s", self._current_water_level)
            return None

    @property
    def water_level_list(self):
        """Get the list of available water level list of the vacuum cleaner."""
        return list(self._water_level_reverse)[1:]

    @property
    def fan_speed_list(self):
        """Get the list of available fan speed steps of the vacuum cleaner."""
        return list(self._fan_speeds_reverse)[1:]

    @property
    def extra_state_attributes(self):
        """Return the specific state attributes of this vacuum cleaner."""
        if self.vacuum_state is not None:
            return {
                ATTR_STATUS: STATE_CODE_TO_STATE[self.vacuum_state],
                ATTR_WATERBOX_STATUS: WATERBOX_CODE_TO_NAME.get(
                    self._waterbox_status, "Unknown"
                ),
                ATTR_OPERATION_STATUS: OPERATION_STATUS_CODE_TO_NAME.get(
                    self._operation_status, "Unknown"
                ),
                ATTR_OPERATING_MODE: OPERATING_MODE_CODE_TO_NAME.get(
                    self._operating_mode, "Unknown"
                ),
                ATTR_ERROR: ERROR_CODE_TO_ERROR.get(self.vacuum_error, "Unknown"),
                ATTR_CARPET_BOOST: self._carpet_boost,
                ATTR_MULTI_MAP_ENABLED: self._multi_map_enabled,
                ATTR_DND_ENABLED: self._dnd_enabled,
                ATTR_DND_START_TIME: self._dnd_start_time,
                ATTR_DND_STOP_TIME: self._dnd_stop_time,
                ATTR_AUDIO_VOLUME: self._audio_volume,
                ATTR_AUDIO_LANGUAGE: self._audio_language,
                ATTR_TIMEZONE: self._timezone,
                ATTR_FAN_SPEED: SPEED_CODE_TO_NAME.get(
                    self._current_fan_speed, "Unknown"
                ),
                ATTR_MAIN_BRUSH_LEFT_TIME: self._main_brush_time_left,
                ATTR_MAIN_BRUSH_LIFE_LEVEL: self._main_brush_life_level,
                ATTR_SIDE_BRUSH_LEFT_TIME: self._side_brush_time_left,
                ATTR_SIDE_BRUSH_LIFE_LEVEL: self._side_brush_life_level,
                ATTR_FILTER_LIFE_LEVEL: self._filter_life_level,
                ATTR_FILTER_LEFT_TIME: self._filter_left_time,
                ATTR_CLEANING_AREA: self._cleaning_area,
                ATTR_CLEANING_TIME: self._cleaning_time,
                ATTR_CLEANING_LOG_START: time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(self._total_log_start)
                ),
                ATTR_CLEANING_TOTAL_TIME: self._total_clean_time,
                ATTR_CLEANING_TOTAL_COUNT: self._total_clean_count,
                ATTR_CLEANING_TOTAL_AREA: self._total_clean_area,
                ATTR_CLEAN_CLOTH_TIP: self._clean_cloth_tip,
                ATTR_SERIAL_NUMBER: self._serial_number,
                ATTR_WATER_LEVEL: WATER_CODE_TO_NAME.get(
                    self._current_water_level, "Unknown"
                ),
                ATTR_WATER_LEVEL_LIST: self.water_level_list,
                ATTR_MAP_ID_LIST: dict(
                    zip(
                        list(
                            "map_" + str(x)
                            for x in range(len(self._schedule.split(";")))
                            if len(self._schedule) > 0
                        ),
                        list(
                            int(x.split("-")[5])
                            for x in self._schedule.split(";")
                            if len(self._schedule) > 0
                        ),
                    )
                ),
                ATTR_ROOM_LIST: dict(
                    zip(
                        list(
                            "map_" + str(x)
                            for x in range(len(self._schedule.split(";")))
                            if len(self._schedule) > 0
                        ),
                        list(
                            [
                                chr(int(item) + 64)
                                for item in list(
                                    x.split(",")
                                    for x in list(
                                        x.split("-")[8]
                                        for x in self._schedule.split(";")
                                    )
                                )[i]
                            ]
                            for i in range(len(self._schedule.split(";")))
                            if len(self._schedule) > 0
                        ),
                    )
                ),
            }

    @property
    def supported_features(self):
        """Flag vacuum cleaner robot features that are supported."""
        return SUPPORT_XIAOMI

    async def _try_command(self, mask_error, func, *args, **kwargs):
        """Call a vacuum command handling error messages."""
        try:
            await self.hass.async_add_executor_job(partial(func, *args, **kwargs))
            return True
        except DeviceException as exc:
            _LOGGER.error(mask_error, exc)
            return False

    async def async_locate(self, **kwargs):
        """Locate the vacuum cleaner."""
        await self._try_command("Unable to locate the botvac: %s", self._vacuum.locate)

    async def async_start(self):
        """Start or resume the cleaning task."""
        await self._try_command(
            "Unable to start the vacuum: %s", self._vacuum.start_sweep
        )

    async def async_stop(self, **kwargs):
        """Stop the vacuum cleaner."""
        await self._try_command("Unable to stop: %s", self._vacuum.stop_sweeping)

    async def async_clean_zone(self, zone, repeats):
        """Clean selected area."""
        await self._try_command(
            "Unable to send zoned_clean command to the vacuum: %s",
            self._vacuum.zone_cleanup,
            zone,
            repeats,
        )

    async def async_clean_room_by_id(self, rooms, repeats, clean_mode, mop_mode):
        """Clean selected room using id."""
        await self._try_command(
            "Unable to send room_cleanup_by_id command to the vacuum: %s",
            self._vacuum.room_cleanup_by_id,
            rooms,
            repeats,
            clean_mode,
            mop_mode,
        )

    async def async_set_restricted_zone(self, walls="", zones="", mops=""):
        """Create restricted zone."""
        await self._try_command(
            "Unable to send set_restricted_zone command to the vacuum: %s",
            self._vacuum.set_restricted_zone,
            walls,
            zones,
            mops,
        )

    async def async_remote_control_move_step(
        self, rotation: int = 0, velocity: int = 0, duration: int = 1500
    ):
        """Remote control the robot."""
        await self._try_command(
            "Unable to send remote control step command to the vacuum: %s",
            self._vacuum.remote_control_step,
            rotation,
            velocity,
        )

    async def async_reset_filter_life(self):
        """Reset filter life."""
        await self._try_command(
            "Unable to send reset_filter_life command to the vacuum: %s",
            self._vacuum.reset_filter_life,
        )

    async def async_reset_main_brush_life(self):
        """Reset filter life."""
        await self._try_command(
            "Unable to send reset_main_brush_life command to the vacuum: %s",
            self._vacuum.reset_brush_life,
        )

    async def async_reset_side_brush_life(self):
        """Reset filter life."""
        await self._try_command(
            "Unable to send reset_side_brush_life command to the vacuum: %s",
            self._vacuum.reset_side_brush_life,
        )

    async def async_pause(self):
        """Pause the cleaning task."""
        await self._try_command(
            "Unable to set start/pause: %s", self._vacuum.pause_sweeping
        )

    async def async_return_to_base(self, **kwargs):
        """Set the vacuum cleaner to return to the dock."""
        await self._try_command("Unable to return home: %s", self._vacuum.return_home)

    async def async_set_fan_speed(self, fan_speed, **kwargs):
        """Set fan speed."""
        if fan_speed in self._fan_speeds_reverse:
            fan_speed = self._fan_speeds_reverse[fan_speed]
        else:
            try:
                fan_speed = int(fan_speed)
            except ValueError as exc:
                _LOGGER.error(
                    "Fan speed step not recognized (%s). Valid speeds are: %s",
                    exc,
                    self.fan_speed_list,
                )
                return
        await self._try_command(
            "Unable to set fan speed: %s", self._vacuum.set_fan_speed, fan_speed
        )

    async def async_select_map(self, map_id):
        """Switch selected map."""
        await self._try_command(
            "Unable to switch to selected map: %s", self._vacuum.select_map, map_id
        )

    async def async_fast_map(self):
        """Fast map."""
        await self._try_command(
            "Unable to send fast_map command to the vacuum: %s", self._vacuum.fast_map
        )

    async def async_set_water_level(self, water_level, **kwargs):
        """Set water level."""
        if water_level in self._water_level_reverse:
            water_level = self._water_level_reverse[water_level]
        else:
            try:
                water_level = int(water_level)
            except ValueError as exc:
                _LOGGER.error(
                    "water level step not recognized (%s). Valid are: %s",
                    exc,
                    self.water_level_list,
                )
                return
        await self._try_command(
            "Unable to set water level: %s", self._vacuum.set_water_level, water_level
        )

    async def async_multi_map(self, multi_map_enabled=""):
        """Enable or Disable multi map feature"""
        if multi_map_enabled != "" and (
            bool(multi_map_enabled) == True or bool(multi_map_enabled) == False
        ):
            await self._try_command(
                "Unable to set multi map: %s",
                self._vacuum.set_multi_map,
                multi_map_enabled,
            )

    async def async_rename_map(self, map_id="", map_name=""):
        """Rename a map"""
        if map_id != "" and map_name != "":
            await self._try_command(
                "Unable to rename map: %s", self._vacuum.rename_map, map_id, map_name
            )

    async def async_do_not_disturb(self, dnd_enabled="", dnd_start="", dnd_stop=""):
        """Set do not disturb function"""
        if dnd_enabled != "" and (
            bool(dnd_enabled) == True or bool(dnd_enabled) == False
        ):
            await self._try_command(
                "Unable to set DnD mode: %s", self._vacuum.set_dnd, dnd_enabled
            )
        if dnd_start:
            if re.match(self.time_pattern, dnd_start):
                await self._try_command(
                    "Unable to set DnD start time: %s",
                    self._vacuum.set_dnd_start,
                    dnd_start,
                )
            else:
                _LOGGER.error("DnD start time is not valid: (%s).", dnd_start)
        if dnd_stop:
            if re.match(self.time_pattern, dnd_stop):
                await self._try_command(
                    "Unable to set DnD stop time: %s",
                    self._vacuum.set_dnd_stop,
                    dnd_stop,
                )
            else:
                _LOGGER.error("DnD stop time is not valid: (%s).", dnd_stop)

    async def async_set_carpet_boost(self, carpet_boost_enabled):
        """Enable or disable carpet boost function"""
        if carpet_boost_enabled != "" and (
            bool(carpet_boost_enabled) == True or bool(carpet_boost_enabled) == False
        ):
            await self._try_command(
                "Unable to set carpet boost mode: %s",
                self._vacuum.set_carpet_boost,
                carpet_boost_enabled,
            )

    async def async_set_audio_volume(self, volume):
        """Set audio volume"""
        await self._try_command(
            "Unable to set the volume: %s",
            self._vacuum.set_audio_volume,
            volume,
        )
        await self._try_command(
            "Unable to play the sound test: %s", self._vacuum.test_sound
        )

    async def async_install_voice_pack(self, lang_id, url, md5, size, **kwargs):
        """install a custom language pack"""
        await self._try_command(
            "Unable to install language pack: %s",
            self._vacuum.install_voice_pack,
            lang_id,
            url,
            md5,
            size,
        )

    async def async_set_clean_cloth_tip(self, delay):
        """Set reminder delay for cleaning mop, 0 to disable the tip"""
        await self._try_command(
            "Unable to set clean cloth reminder's delay pack: %s",
            self._vacuum.set_cloth_cleaning_tip,
            delay,
        )

    def update(self):
        """Fetch state from the device."""
        try:
            state = self._vacuum.status()
            if (
                not self._no_sleep_when_docked
                or state.status != VacuumStatus.Idle
                or self.vacuum_state != VacuumStatus.Charging
            ):
                self.vacuum_last_state = self.vacuum_state
                self.vacuum_state = state.status
            self.vacuum_error = state.error

            self._fan_speeds = SPEED_CODE_TO_NAME
            self._fan_speeds_reverse = {v: k for k, v in self._fan_speeds.items()}

            self.battery_percentage = state.battery

            self._total_clean_count = state.total_clean_count
            self._total_clean_time = state.total_clean_time
            self._total_log_start = state.total_log_start
            self._total_clean_area = state.total_clean_area

            self._current_fan_speed = state.fan_speed

            self._main_brush_time_left = state.main_brush_left_time
            self._main_brush_life_level = state.main_brush_life_level

            self._side_brush_time_left = state.side_brush_left_time
            self._side_brush_life_level = state.side_brush_life_level

            self._filter_life_level = state.filter_life_level
            self._filter_left_time = state.filter_left_time

            self._cleaning_area = state.cleaning_area
            self._cleaning_time = state.cleaning_time

            self._waterbox_status = state.waterbox_status
            self._water_level = WATER_CODE_TO_NAME
            self._water_level_reverse = {v: k for k, v in self._water_level.items()}
            self._current_water_level = state.water_level

            self._operation_status = state.operation_status
            self._operating_mode = state.operating_mode
            self._schedule = state.schedule if state.schedule is not None else ""

            self._carpet_boost = state.carpet_boost

            self._multi_map_enabled = state.multi_map_enabled

            self._dnd_enabled = state.dnd_enabled
            self._dnd_start_time = state.dnd_start_time
            self._dnd_stop_time = state.dnd_stop_time

            self._audio_volume = state.audio_volume
            self._audio_language = state.audio_language

            self._timezone = state.timezone

            self._clean_cloth_tip = state.clean_cloth_tip

            self._serial_number = state.serial_number

        except OSError as exc:
            _LOGGER.error("Got OSError while fetching the state: %s", exc)

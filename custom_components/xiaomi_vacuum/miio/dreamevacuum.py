import logging
from dataclasses import dataclass, field

import click
from .click_common import command
from .miot_device import DeviceStatus as DeviceStatusContainer
from .miot_device import MiotDevice, MiotMapping
from .dreame_const import *

from random import randint

_LOGGER = logging.getLogger(__name__)


class DreameVacuumStatus(DeviceStatusContainer):
    def __init__(self, data):
        self.data = data

    @property
    def status(self) -> VacuumStatus:
        try:
            return VacuumStatus(self.data["property_device_status"])
        except ValueError:
            _LOGGER.error(
                "Unknown device_status (%s)", self.data["property_device_status"]
            )
            return VacuumStatus.Unknown

    @property
    def error(self) -> ErrorCodes:
        try:
            return ErrorCodes(self.data["property_device_fault"])
        except ValueError:
            _LOGGER.error(
                "Unknown device_fault (%s)", self.data["property_device_fault"]
            )
            return ErrorCodes.Unknown

    @property
    def battery(self) -> int:
        return self.data["property_battery_level"]

    @property
    def state(self) -> ChargeStatus:
        try:
            return ChargeStatus(self.data["property_charging_state"])
        except ValueError:
            _LOGGER.error(
                "Unknown charging_state (%s)", self.data["property_charging_state"]
            )
            return ChargeStatus.Unknown

    @property
    def operating_mode(self) -> OperatingMode:
        try:
            return OperatingMode(self.data["property_operating_mode"])
        except ValueError:
            _LOGGER.error(
                "Unknown operating_mode (%s)", self.data["property_operating_mode"]
            )
            return OperatingMode.Unknown

    @property
    def cleaning_time(self) -> str:
        return self.data["property_cleaning_time"]

    @property
    def cleaning_area(self) -> str:
        return self.data["property_cleaning_area"]

    @property
    def fan_speed(self) -> VacuumSpeed:
        try:
            return VacuumSpeed(self.data["property_cleaning_mode"])
        except ValueError:
            _LOGGER.error(
                "Unknown cleaning_mode (%s)", self.data["property_cleaning_mode"]
            )
            return VacuumSpeed.Unknown

    @property
    def water_level(self) -> WaterLevel:
        try:
            return WaterLevel(self.data["property_water_level"])
        except ValueError:
            _LOGGER.error("Unknown water_level (%s)", self.data["property_water_level"])
            return WaterLevel.Unknown

    @property
    def waterbox_status(self) -> Waterbox:
        try:
            return Waterbox(self.data["property_waterbox_status"])
        except ValueError:
            _LOGGER.error(
                "Unknown waterbox_status (%s)", self.data["property_waterbox_status"]
            )
            return Waterbox.Unknown

    @property
    def operation_status(self) -> OperationStatus:
        try:
            return OperationStatus(self.data["property_operation_status"])
        except ValueError:
            _LOGGER.error(
                "Unknown operation_status (%s)", self.data["property_operation_status"]
            )
            return OperationStatus.Unknown

    @property
    def carpet_boost(self) -> bool:
        return bool(self.data["property_carpet_boost"])

    @property
    def multi_map_enabled(self) -> bool:
        return bool(self.data["property_multi_map_enabled"])

    @property
    def dnd_enabled(self) -> bool:
        return self.data["property_dnd_enabled"]

    @property
    def dnd_start_time(self) -> str:
        return self.data["property_dnd_start_time"]

    @property
    def dnd_stop_time(self) -> str:
        return self.data["property_dnd_stop_time"]

    @property
    def audio_volume(self) -> int:
        return self.data["property_audio_volume"]

    @property
    def audio_language(self) -> str:
        return self.data["property_audio_language"]

    @property
    def timezone(self) -> str:
        return self.data["property_timezone"]

    @property
    def schedule(self) -> str:
        return self.data["property_scheduled-clean"]

    @property
    def main_brush_left_time(self) -> int:
        return self.data["property_main_brush_left_time"]

    @property
    def main_brush_life_level(self) -> int:
        return self.data["property_main_brush_life_level"]

    @property
    def side_brush_left_time(self) -> int:
        return self.data["property_side_brush_left_time"]

    @property
    def side_brush_life_level(self) -> int:
        return self.data["property_side_brush_life_level"]

    @property
    def filter_life_level(self) -> int:
        return self.data["property_filter_life_level"]

    @property
    def filter_left_time(self) -> int:
        return self.data["property_filter_left_time"]

    @property
    def total_log_start(self) -> int:
        return self.data["property_first-clean-time"]

    @property
    def total_clean_time(self) -> int:
        return self.data["property_total_clean_time"]

    @property
    def total_clean_count(self) -> int:
        return self.data["property_total_clean_count"]

    @property
    def total_clean_area(self) -> int:
        return self.data["property_total_clean_area"]

    @property
    def clean_cloth_tip(self) -> str:
        return self.data["property_clean_cloth_tip"]

    @property
    def serial_number(self) -> str:
        return self.data["property_serial_number"]


class DreameVacuum(MiotDevice):
    """Support for dreame vacuum robot d9 (dreame.vacuum.p2009)."""

    mapping = DreameD9Mapping

    def status(self) -> DreameVacuumStatus:
        """State of the vacuum."""

        return DreameVacuumStatus(
            {
                prop["did"]: (prop["value"] if "value" in prop.keys() else None) if prop["code"] == 0 else None
                for prop in self.get_properties_for_mapping()
            }
        )

    @command(click.argument("speed", type=int))
    def set_fan_speed(self, speed):
        """Set vacuum cleaning mode."""
        return self.set_property("property_cleaning_mode", speed)

    @command()
    def return_home(self) -> None:
        """Return home for charging."""
        return self.call_action("action_start_charging")

    @command()
    def start_sweep(self) -> None:
        """Start cleaning."""
        return self.call_action("action_start_sweeping")

    @command()
    def pause_sweeping(self) -> None:
        """Pause cleaning."""
        return self.call_action("action_pause_sweeping")

    @command()
    def reset_brush_life(self) -> None:
        """Reset main brush's life."""
        return self.call_action("action_reset_main_brush_life")

    @command()
    def reset_filter_life(self) -> None:
        """Reset filter's life."""
        return self.call_action("action_reset_filter_life")

    @command()
    def reset_side_brush_life(self) -> None:
        """Reset side brush's life."""
        return self.call_action("action_reset_side_brush_life")

    @command()
    def start_sweeping_advanced(self, params) -> None:
        """Start cleaning (advanced). Specify cleaning mode like room, zone,..."""
        return self.call_action("action_start_sweeping_advanced", params)

    @command()
    def stop_sweeping(self) -> None:
        """Stop cleaning."""
        return self.call_action("action_stop_sweeping")

    @command()
    def set_map(self, params) -> None:
        """Set map related features like: switching to another map, setting restricted area, etc."""
        return self.call_action("action_set_map", params)

    @command()
    def fast_map(self) -> None:
        """Start fast mapping."""
        payload = [{"piid": 1, "value": 21}]
        return self.start_sweeping_advanced(payload)

    @command()
    def set_carpet_boost(self, carpet_boost_enabled) -> None:
        """Enable or disable carpet boost."""
        return self.set_property(
            "property_carpet_boost", 1 if carpet_boost_enabled else 0
        )

    @command()
    def set_multi_map(self, multi_map_enabled) -> None:
        """Enable or disable multi map feature."""
        return self.set_property(
            "property_multi_map_enabled", 1 if multi_map_enabled else 0
        )

    @command()
    def rename_map(self, map_id, map_name) -> None:
        """Rename a map"""
        payload = [
            {
                "piid": 4,
                "value": '{"nrism":{%(id)s:{"name":%(name)s} } }'
                % {"id": map_id, "name": map_name},
            },
        ]
        return self.call_action("action_set_map", payload)

    @command()
    def set_dnd(self, dnd_enabled) -> None:
        """Enable or disable do not disturb."""
        return self.set_property("property_dnd_enabled", dnd_enabled)

    @command()
    def set_dnd_start(self, dnd_start) -> None:
        """set start time for do not disturb function."""
        return self.set_property("property_dnd_start_time", dnd_start)

    @command()
    def set_dnd_stop(self, dnd_stop) -> None:
        """set end time for do not disturb function."""
        return self.set_property("property_dnd_stop_time", dnd_stop)

    @command(click.argument("coords", type=str), click.argument("repeats", type=int))
    def zone_cleanup(self, coords, repeats) -> None:
        """Start zone cleaning."""
        payload = [
            {"piid": 1, "value": 19},
            {
                "piid": 10,
                "value": '{"areas": [[%(coords)s,%(repeats)d,0,0]]}'
                % {"coords": coords, "repeats": repeats},
                # TODO find out why the two last parameters do not affect fan speed or water level / what do they do?
            },
        ]
        return self.start_sweeping_advanced(payload)

    @command()
    def room_cleanup_by_id(self, rooms, repeats, clean_mode, mop_mode) -> None:
        """Start room-id cleaning."""
        cleanlist = []
        for sublist in rooms:
            if len(sublist) > 1:
                repeats = sublist[1]
            if len(sublist) > 2:
                clean_mode = sublist[2]
            if len(sublist) > 3:
                mop_mode = sublist[3]
            cleanlist.append(
                [
                    ord(sublist[0].upper()) - 64,
                    repeats,
                    clean_mode,
                    mop_mode,
                    rooms.index(sublist) + 1,
                ]
            )
        payload = [
            {"piid": 1, "value": 18},
            {
                "piid": 10,
                "value": '{"selects": ' + str(cleanlist).replace(" ", "") + "}",
            },
        ]
        return self.start_sweeping_advanced(payload)

    @command(
        click.argument("walls", type=str),
        click.argument("zones", type=str),
        click.argument("mops", type=str),
    )
    def set_restricted_zone(self, walls, zones, mops) -> None:
        """set restricted/ no-mop zone"""
        value = '{"vw":{"line":[%(walls)s],"rect":[%(zones)s],"mop":[%(mops)s]}}' % {
            "walls": walls,
            "zones": zones,
            "mops": mops,
        }
        payload = [{"piid": 4, "value": value}]
        return self.set_map(payload)

    @command()
    def remote_control_step(self, rotation, velocity) -> None:
        """
        Move robot manually one time.
        :param int rotation: angle to rotate in binary angles 128 to -128
        :param int velocity: speed to move forward or backward 100 to -300
        """
        value = '{"spdv":%(velocity)d,"spdw":%(rotation)d,"audio":"false"}' % {
            "velocity": velocity,
            "rotation": rotation,
        }
        return self.set_property("property_remote_control_step", value)

    @command()
    def request_map(self, params) -> None:
        # TODO find out the parameters
        return self.call_action("action_req_map", params)

    @command()
    def select_map(self, map_id) -> None:
        """Switch to another map."""
        payload = [
            {
                "piid": 4,
                "value": '{"sm": ' + "{" + "}" + ', "mapid":' + str(map_id) + "}",
            }
        ]
        return self.set_map(payload)

    @command(click.argument("water", type=int))
    def set_water_level(self, water):
        """Set water level"""
        return self.set_property("property_water_level", water)

    @command()
    def locate(self) -> None:
        """Locate vacuum robot."""
        return self.call_action("action_locate")

    @command()
    def install_voice_pack(self, lang_id: str, url: str, md5: str, size: int) -> None:
        """Install given voice pack."""
        value = (
            '{"id":"%(lang_id)s","url":"%(url)s","md5":"%(md5)s","size":%(size)d}'
            % {"lang_id": lang_id, "url": url, "md5": md5, "size": size}
        )
        self.set_property("property_voice", value)

    @command(click.argument("volume", type=int))
    def set_audio_volume(self, volume):
        """Set voice audio volume"""
        return self.set_property("property_audio_volume", volume)

    @command()
    def test_sound(self) -> None:
        """Plays a confirmation sound to check the volume"""
        return self.call_action("action_test_sound")

    @command(click.argument("time", type=int))
    def set_cloth_cleaning_tip(self, delay):
        """Set reminder delay for cleaning mop, 0 to disable the tip"""
        return self.set_property("property_clean_cloth_tip", delay)

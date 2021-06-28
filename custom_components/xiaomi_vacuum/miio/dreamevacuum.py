import logging
from dataclasses import dataclass, field
from enum import IntEnum

import click
from .click_common import command
from .miot_device import DeviceStatus as DeviceStatusContainer
from .miot_device import MiotDevice, MiotMapping

from random import randint

_LOGGER = logging.getLogger(__name__)

_MAPPING: MiotMapping = {
    ## General
    "property_device_status": {"siid": 2, "piid": 1},
    "property_device_fault": {"siid": 2, "piid": 2},
    "action_start_sweeping": {"siid": 2, "aiid": 1},
    "action_pause_sweeping": {"siid": 2, "aiid": 2},
    ## Battery
    "property_battery_level": {"siid": 3, "piid": 1},
    "property_charging_state": {"siid": 3, "piid": 2},
    "action_start_charging": {"siid": 3, "aiid": 1},
    ## Vacuum
    "property_operating_mode": {"siid": 4, "piid": 1},
    "property_cleaning_time": {"siid": 4, "piid": 2},
    "property_cleaning_area": {"siid": 4, "piid": 3},
    "property_cleaning_mode": {"siid": 4, "piid": 4},
    "property_water_level": {"siid": 4, "piid": 5},
    "property_waterbox_status": {"siid": 4, "piid": 6},
    "property_operation_status": {"siid": 4, "piid": 7},
    "property_serial_number": {"siid": 4, "piid": 14},
    "property_remote_control_step": {"siid": 4, "piid": 15},
    "property_clean_cloth_tip": {"siid": 4, "piid": 16},
    "action_start_sweeping_advanced": {"siid": 4, "aiid": 1},
    "action_stop_sweeping": {"siid": 4, "aiid": 2},
    ## Do not disturb
    "property_dnd_enabled": {"siid": 5, "piid": 1},
    "property_dnd_start_time": {"siid": 5, "piid": 2},
    "property_dnd_stop_time": {"siid": 5, "piid": 3},
    ## Map
    "action_req_map": {"siid": 6, "aiid": 1},
    "action_set_map": {"siid": 6, "aiid": 2},
    ## Audio
    "property_audio_volume": {"siid": 7, "piid": 1},
    "property_audio_language": {"siid": 7, "piid": 2},
    "property_voice": {"siid": 7, "piid": 4},
    "action_locate": {"siid": 7, "aiid": 1},
    "action_test_sound": {"siid": 7, "aiid": 2},
    ## Schedule
    "property_timezone": {"siid": 8, "piid": 1},
    "property_scheduled-clean": {"siid": 8, "piid": 2},
    ## Main brush
    "property_main_brush_left_time": {"siid": 9, "piid": 1},
    "property_main_brush_life_level": {"siid": 9, "piid": 2},
    "action_reset_main_brush_life": {"siid": 9, "aiid": 1},
    ## Side brush
    "property_side_brush_left_time": {"siid": 10, "piid": 1},
    "property_side_brush_life_level": {"siid": 10, "piid": 2},
    "action_reset_side_brush_life": {"siid": 10, "aiid": 1},
    ## Filter
    "property_filter_life_level": {"siid": 11, "piid": 1},
    "property_filter_left_time": {"siid": 11, "piid": 2},
    "action_reset_filter_life": {"siid": 11, "aiid": 1},
    ## Log
    "property_first-clean-time": {"siid": 12, "piid": 1},
    "property_total_clean_time": {"siid": 12, "piid": 2},
    "property_total_clean_count": {"siid": 12, "piid": 3},
    "property_total_clean_area": {"siid": 12, "piid": 4},
}


class ChargeStatus(IntEnum):
    Unknown = -1
    Charging = 1
    Not_charging = 2
    Charging2 = 4
    Go_charging = 5


class ErrorCodes(IntEnum):
    Unknown = -1
    NoError = 0
    Drop = 1
    Cliff = 2
    Bumper = 3
    Gesture = 4
    Bumper_repeat = 5
    Drop_repeat = 6
    Optical_flow = 7
    No_box = 8
    No_tankbox = 9
    Waterbox_empty = 10
    Box_full = 11
    Brush = 12
    Side_brush = 13
    Fan = 14
    Left_wheel_motor = 15
    Right_wheel_motor = 16
    Turn_suffocate = 17
    Forward_suffocate = 18
    Charger_get = 19
    Battery_low = 20
    Charge_fault = 21
    Battery_percentage = 22
    Heart = 23
    Camera_occlusion = 24
    Camera_fault = 25
    Event_battery = 26
    Forward_looking = 27
    Gyroscope = 28
    # TODO find out other missing codes
    RouteBlocked = 47


class VacuumStatus(IntEnum):
    Unknown = -1
    Sweeping = 1
    Idle = 2
    Paused = 3
    Error = 4
    Go_charging = 5
    Charging = 6
    Mopping = 7


class VacuumSpeed(IntEnum):
    """Fan speeds, same as for ViomiVacuum."""

    Unknown = -1
    Silent = 0
    Standard = 1
    strong = 2
    Turbo = 3


class Waterbox(IntEnum):
    """Fan speeds, same as for ViomiVacuum."""

    Unknown = -1
    Removed = 0
    Present = 1


class WaterLevel(IntEnum):
    Unknown = -1
    Low = 1
    Medium = 2
    High = 3


class OperationStatus(IntEnum):
    Unknown = -1
    OperationCompleted = 0
    OperationAutoClean = 1
    OperationCustomAreaClean = 2
    OperationAreaClean = 3
    OperationSpotClean = 4
    OperationFastMapping = 5


class OperatingMode(IntEnum):
    Unknown = -1
    IdleMode = 0
    PauseAndStopMode = 1
    AutoCleanMode = 2
    BackHomeMode = 3
    PartCleanMode = 4
    FollowWallMode = 5
    ChargingMode = 6
    OtaModeMode = 7
    FctModeMode = 8
    WIFISetMode = 9
    PowerOffMode = 10
    FactoryMode = 11
    ErrRepotMode = 12
    RemoteCtrlMode = 13
    SleepMode = 14
    SelfTestMode = 15
    FactoryFuncTest = 16
    StandbyMode = 17
    AreaClean = 18
    CustomAreaClean = 19
    SpotClean = 20
    FastMapping = 21


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

    mapping = _MAPPING

    def status(self) -> DreameVacuumStatus:
        """State of the vacuum."""

        return DreameVacuumStatus(
            {
                prop["did"]: prop["value"] if prop["code"] == 0 else None
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

    @command()
    def test_sound(self) -> None:
        """aiid 3 : in: [] -> out: []"""
        return self.call_action("action_test_sound")

    @command(click.argument("time", type=int))
    def set_cloth_cleaning_tip(self, delay):
        """Set reminder delay for cleaning mop, 0 to disable the tip"""
        return self.set_property("property_clean_cloth_tip", delay)

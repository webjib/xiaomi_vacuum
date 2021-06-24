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
    "device_status": {"siid": 2, "piid": 1},
    "device_fault": {"siid": 2, "piid": 2},
    "battery_level": {"siid": 3, "piid": 1},
    "charging_state": {"siid": 3, "piid": 2},
    "operating_mode": {"siid": 4, "piid": 1},
    "cleaning_time": {"siid": 4, "piid": 2},
    "cleaning_area": {"siid": 4, "piid": 3},
    "cleaning_mode": {"siid": 4, "piid": 4},
    "water_level": {"siid": 4, "piid": 5},
    "waterbox_status": {"siid": 4, "piid": 6},
    "operation_status": {"siid": 4, "piid": 7},
    "dnd_enabled": {"siid": 5, "piid": 1},
    "dnd_start_time": {"siid": 5, "piid": 2},
    "dnd_stop_time": {"siid": 5, "piid": 3},
    "audio_volume": {"siid": 7, "piid": 1},
    "audio_language": {"siid": 7, "piid": 2},
    "set-voice": {"siid": 7, "piid": 4},
    "timezone": {"siid": 8, "piid": 1},
    "scheduled-clean": {"siid": 8, "piid": 2},
    "main_brush_left_time": {"siid": 9, "piid": 1},
    "main_brush_life_level": {"siid": 9, "piid": 2},
    "side_brush_left_time": {"siid": 10, "piid": 1},
    "side_brush_life_level": {"siid": 10, "piid": 2},
    "filter_life_level": {"siid": 11, "piid": 1},
    "filter_left_time": {"siid": 11, "piid": 2},
    "first-clean-time": {"siid": 12, "piid": 1},
    "total_clean_time": {"siid": 12, "piid": 2},
    "total_clean_count": {"siid": 12, "piid": 3},
    "total_clean_area": {"siid": 12, "piid": 4},
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
            return VacuumStatus(self.data["device_status"])
        except ValueError:
            _LOGGER.error("Unknown device_status (%s)", self.data["device_status"])
            return VacuumStatus.Unknown

    @property
    def error(self) -> ErrorCodes:
        try:
            return ErrorCodes(self.data["device_fault"])
        except ValueError:
            _LOGGER.error("Unknown device_fault (%s)", self.data["device_fault"])
            return ErrorCodes.Unknown

    @property
    def battery(self) -> int:
        return self.data["battery_level"]

    @property
    def state(self) -> ChargeStatus:
        try:
            return ChargeStatus(self.data["charging_state"])
        except ValueError:
            _LOGGER.error("Unknown charging_state (%s)", self.data["charging_state"])
            return ChargeStatus.Unknown

    @property
    def operating_mode(self) -> OperatingMode:
        try:
            return OperatingMode(self.data["operating_mode"])
        except ValueError:
            _LOGGER.error("Unknown operating_mode (%s)", self.data["operating_mode"])
            return OperatingMode.Unknown

    @property
    def cleaning_time(self) -> str:
        return self.data["cleaning_time"]

    @property
    def cleaning_area(self) -> str:
        return self.data["cleaning_area"]

    @property
    def fan_speed(self) -> VacuumSpeed:
        try:
            return VacuumSpeed(self.data["cleaning_mode"])
        except ValueError:
            _LOGGER.error("Unknown cleaning_mode (%s)", self.data["cleaning_mode"])
            return VacuumSpeed.Unknown

    @property
    def water_level(self) -> WaterLevel:
        try:
            return WaterLevel(self.data["water_level"])
        except ValueError:
            _LOGGER.error("Unknown water_level (%s)", self.data["water_level"])
            return WaterLevel.Unknown

    @property
    def waterbox_status(self) -> Waterbox:
        try:
            return Waterbox(self.data["waterbox_status"])
        except ValueError:
            _LOGGER.error("Unknown waterbox_status (%s)", self.data["waterbox_status"])
            return Waterbox.Unknown

    @property
    def operation_status(self) -> OperationStatus:
        try:
            return OperationStatus(self.data["operation_status"])
        except ValueError:
            _LOGGER.error(
                "Unknown operation_status (%s)", self.data["operation_status"]
            )
            return OperationStatus.Unknown

    @property
    def dnd_enabled(self) -> bool:
        return self.data["dnd_enabled"]

    @property
    def dnd_start_time(self) -> str:
        return self.data["dnd_start_time"]

    @property
    def dnd_stop_time(self) -> str:
        return self.data["dnd_stop_time"]

    @property
    def audio_volume(self) -> int:
        return self.data["audio_volume"]

    @property
    def audio_language(self) -> str:
        return self.data["audio_language"]

    @property
    def timezone(self) -> str:
        return self.data["timezone"]

    @property
    def schedule(self) -> str:
        return self.data["scheduled-clean"]

    @property
    def main_brush_left_time(self) -> int:
        return self.data["main_brush_left_time"]

    @property
    def main_brush_life_level(self) -> int:
        return self.data["main_brush_life_level"]

    @property
    def side_brush_left_time(self) -> int:
        return self.data["side_brush_left_time"]

    @property
    def side_brush_life_level(self) -> int:
        return self.data["side_brush_life_level"]

    @property
    def filter_life_level(self) -> int:
        return self.data["filter_life_level"]

    @property
    def filter_left_time(self) -> int:
        return self.data["filter_left_time"]

    @property
    def total_log_start(self) -> int:
        return self.data["first-clean-time"]

    @property
    def total_clean_time(self) -> int:
        return self.data["total_clean_time"]

    @property
    def total_clean_count(self) -> int:
        return self.data["total_clean_count"]

    @property
    def total_clean_area(self) -> int:
        return self.data["total_clean_area"]


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

    def call_action(self, siid, aiid, params=None):
        # {"did":"call-siid-aiid","siid":18,"aiid":1,"in":[{"piid":1,"value":2}]
        if params is None:
            params = []
        payload = {
            "did": f"call-{siid}-{aiid}",
            "siid": siid,
            "aiid": aiid,
            "in": params,
        }
        return self.send("action", payload)

    @command(click.argument("speed", type=int))
    def set_fan_speed(self, speed):
        return self.set_property("cleaning_mode", speed)

    # siid 3: (Battery): 2 props, 1 actions
    # aiid 1 Start Charge: in: [] -> out: []
    @command()
    def return_home(self) -> None:
        """aiid 1 Start Charge: in: [] -> out: []"""
        return self.call_action(3, 1)

    # siid 2: (Robot Cleaner): 2 props, 2 actions
    # aiid 1 Start Sweep: in: [] -> out: []
    @command()
    def start_sweep(self) -> None:
        """aiid 1 Start Sweep: in: [] -> out: []"""
        return self.call_action(2, 1)

    # aiid 2 Stop Sweeping: in: [] -> out: []
    @command()
    def stop_sweeping(self) -> None:
        """aiid 2 Stop Sweeping: in: [] -> out: []"""
        return self.call_action(2, 2)

    # siid 9: (Main Cleaning Brush): 2 props, 1 actions
    # aiid 1: Reset Brush Life: in: [] -> out: []
    @command()
    def reset_brush_life(self) -> None:
        """aiid 1 Reset Brush Life: in: [] -> out: []"""
        return self.call_action(9, 1)

    # siid 11: (Filter): 2 props, 1 actions
    # aiid 1: Reset Filter Life: in: [] -> out: []
    @command()
    def reset_filter_life(self) -> None:
        """aiid 1 Reset Filter Life: in: [] -> out: []"""
        return self.call_action(11, 1)

    # siid 10: (Side Cleaning Brush): 2 props, 1 actions
    # aiid 1: Reset Brush Life: in: [] -> out: []
    @command()
    def reset_side_brush_life(self) -> None:
        """aiid 1 Reset Brush Life: in: [] -> out: []"""
        return self.call_action(10, 1)

    # siid 4: (vacuum-extend): 20 props, 3 actions
    # aiid 1: (start-clean): in: [] -> out: []
    @command()
    def start(self) -> None:
        """Start cleaning."""
        # TODO: find out other values
        payload = [{"piid": 1, "value": 2}]
        return self.call_action(4, 1, payload)

    # aiid 2 stop-clean: in: [] -> out: []
    @command()
    def stop(self) -> None:
        """Stop cleaning."""
        return self.call_action(4, 2)

    # aiid 4 fast mapping
    @command()
    def fast_map(self) -> None:
        """Start fast mapping."""
        payload = [{"piid": 1, "value": 21}]
        return self.call_action(4, 1, payload)

    @command(click.argument("coords", type=str))
    def zone_cleanup(self, coords) -> None:
        """Start zone cleaning."""
        payload = [{"piid": 1, "value": 19}, {"piid": 10, "value": coords}]
        return self.call_action(4, 1, payload)
        # # siid 21: (remote): 2 props, 3 actions

    # @command(click.argument("coords", type=str, ""))
    def room_cleanup_by_id(self, rooms, repeats, clean_mode, mop_mode) -> None:
        """Start room-id cleaning."""
        # clean_mode = 3
        # mop_mode = 3
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
        return self.call_action(4, 1, payload)

    @command(click.argument("coords", type=str))
    def restricted_zone(self, coords) -> None:
        """Create restricted/mop zone"""
        payload = [{"piid": 4, "value": coords}]
        return self.call_action(6, 2, payload)

    @command()
    def manual_control_once(self, rotation, velocity) -> None:
        siid = 4
        piid = 15
        payload = [
            {
                "did": f"call-{siid}-{piid}",
                "siid": 4,
                "piid": 15,
                "value": '{"spdv": '
                + str(velocity)
                + ',"spdw": '
                + str(rotation)
                + ',"audio":"false","random": '
                + str(randint(1000, 9999))
                + "}",
            }
        ]
        return self.send("set_properties", payload)

    # siid 6: (map): 6 props, 2 actions
    # aiid 1: (map-req): in: [2] -> out: []
    @command()
    def map_req(self) -> None:
        return self.call_action(6, 1)

    # aiid 2: (set-map)
    @command()
    def set_map(self, map_id) -> None:
        payload = [
            {
                "piid": 4,
                "value": '{"sm": ' + "{" + "}" + ', "mapid":' + str(map_id) + "}",
            }
        ]
        return self.call_action(6, 2, payload)

    @command(click.argument("water", type=int))
    def set_water_level(self, water):
        """Set water level"""
        return self.set_property("water_level", water)

    # siid 7: (audio): 4 props, 2 actions
    # aiid 1: in: [] -> out: []
    @command()
    def find(self) -> None:
        """Locate Vacuum Robot"""
        return self.call_action(7, 1)

    # aiid 2 : in: [] -> out: []
    @command()
    def install_voice_pack(self, lang_id: str, url: str, md5: str, size: int) -> None:
        """Install given voice pack."""
        value = (
            '{"id":"%(lang_id)s","url":"%(url)s","md5":"%(md5)s","size":%(size)d}'
            % {"lang_id": lang_id, "url": url, "md5": md5, "size": size}
        )
        _LOGGER.info("pooya: " + value)
        self.set_property(
            "set-voice",
            '{"id":"%(lang_id)s","url":"%(url)s","md5":"%(md5)s","size":%(size)d}'
            % {"lang_id": lang_id, "url": url, "md5": md5, "size": size},
        )

    # aiid 2: in: [] -> out: []
    @command()
    def test_sound(self) -> None:
        """aiid 3 : in: [] -> out: []"""
        return self.call_action(7, 2)

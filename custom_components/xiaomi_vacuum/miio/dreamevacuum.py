import logging
from dataclasses import dataclass, field
from enum import Enum

import click
from .click_common import command
from .miot_device import MiotDevice

from random import randint

_LOGGER = logging.getLogger(__name__)


class ChargeStatus(Enum):
    Charging = 1
    Not_charging = 2
    Charging2 = 4
    Go_charging = 5


class Error(Enum):
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


class VacuumStatus(Enum):
    Sweeping = 1
    Idle = 2
    Paused = 3
    Error = 4
    Go_charging = 5
    Charging = 6
    Mopping = 7


class VacuumSpeed(Enum):
    """Fan speeds, same as for ViomiVacuum."""

    Silent = 0
    Standard = 1
    Medium = 2
    Turbo = 3


class Waterbox(Enum):
    """Fan speeds, same as for ViomiVacuum."""

    Removed = 0
    Present = 1

class WaterLevel(Enum):
    Low = 1
    Medium = 2
    High = 3

class taskStatus(Enum):

    TaskCompleted = 0
    TaskAutoClean = 1
    TaskCustomAreaClean = 2
    TaskAreaClean = 3
    TaskSpotClean = 4
    TaskFastMapping = 5

class  WorkMode(Enum):

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

@dataclass
class DreameStatus:
    _max_properties = 14

    # siid 2: (Robot Cleaner): 2 props, 2 actions
    # piid: 2 (Device Fault): (uint8, unit: None) (acc: ['read', 'notify'], value-list: [{'value': 0, 'description': 'No faults'}], value-range: None)
    error: int = field(
        metadata={
            "siid": 2,
            "piid": 2,
            "access": ["read", "notify"],
            "enum": Error
        },
        default=None
    )
    # piid: 1 (Status): (int8, unit: None) (acc: ['read', 'notify'], value-list: [{'value': 1, 'description': 'Sweeping'}, {'value': 2, 'description': 'Idle'}, {'value': 3, 'description': 'Paused'}, {'value': 4, 'description': 'Error'}, {'value': 5, 'description': 'Go Charging'}, {'value': 6, 'description': 'Charging'}], value-range: None)
    status: int = field(
        metadata={
            "siid": 2,
            "piid": 1,
            "access": ["read", "notify"],
            "enum": VacuumStatus,
        },
        default=None
    )

    # siid 3: (Battery): 2 props, 1 actions
    # piid: 1 (Battery Level): (uint8, unit: percentage) (acc: ['read', 'notify'], value-list: [], value-range: [0, 100, 1])
    battery: int = field(
        metadata={
            "siid": 3,
            "piid": 1,
            "access": ["read", "notify"]
        },
        default=None)
        
    # piid: 2 (Charging State): (uint8, unit: None) (acc: ['read', 'notify'], value-list: [{'value': 1, 'description': 'Charging'}, {'value': 2, 'description': 'Not Charging'}, {'value': 5, 'description': 'Go Charging'}], value-range: None)
    state: int = field(
        metadata={
            "siid": 3,
            "piid": 2,
            "access": ["read", "notify"],
            "enum": ChargeStatus,
        },
        default=None
    )

    # siid 4: (Sweeper extended function protocol): 15 props, 2 actions
    # piid: 1 (work-mode): (int32, unit: none) (acc: ['read', 'notify'], value-list: [], value-range: [0, 50, 1])
    operating_mode: int = field(
        metadata={"siid": 4,
            "piid": 1,
            "access": ["read", "notify"]
        },
        default=None
    )
    
    # piid: 2 (timer): (string, unit: minute) (acc: ['read', 'notify'], value-list: [], value-range: [0, 32767, 1])
    timer: str = field(
        metadata={"siid": 4,
        "piid": 2,
        "access": ["read", "notify"]
        },
        default=None)
    
    # piid: 3 (area): (string, unit: None) (acc: ['read', 'notify'], value-list: [], value-range: [0, 32767, 1])
    area: str = field(
        metadata={"siid": 4,
        "piid": 3,
        "access": ["read", "notify"]
        },
        default=None)
    
    # piid: 4 (Cleaning-mode): (int8, unit: none) (acc: ['read', 'notify', 'write'], value-list: [{'value': 0, 'description': 'Quiet'}, {'value': 1, 'description': 'Standard'}, {'value': 2, 'description': 'Strong'}, {'value': 3, 'description': 'Turbo'}])
    fan_speed: int = field(
        metadata={
            "siid": 4,
            "piid": 4,
            "access": ["read", "notify", "write"],
            "enum": VacuumSpeed,
        },
        default=None
    )

    # piid: 5 (mop-mode): (int8, unit: none) (acc: ['read', 'notify', 'write'], value-list: [{'value': 1, 'description': 'low'}, {'value': 2, 'description': 'medium'}, {'value': 3, 'description': 'high'}])
    water_level: int = field(
        metadata={
            "siid": 4,
            "piid": 5,
            "access": ["read", "write", "notify"],
            "enum": WaterLevel,
        },
        default=None
    )

    # piid: 6 (waterbox-status): (int8, unit: none) (acc: ['read', 'notify', 'write'], value-list: [{'value': 0, 'description': ''}, {'value': 1, 'description': 'medium'}])
    waterbox_status: int = field(
        metadata={
            "siid": 4,
            "piid": 6,
            "access": ["read", "notify", "write"],
            "enum": Waterbox,
        },
        default=None
    )


    # siid 5: (do-not-disturb): 3 props, 0 actions
    # piid: 1 (enable): (bool, unit: None) (acc: ['read', 'notify', 'write'], value-list: [], value-range: None)
    dnd_enabled: bool = field(
        metadata={
            "siid": 5,
            "piid": 1,
            "access": ["read", "notify", "write"]
        },
        default=None
    )
    
    # piid: 2 (start-time): (string, unit: None) (acc: ['read', 'notify', 'write'], value-list: [], value-range: None)
    dnd_start_time: str = field(
        metadata={
            "siid": 5,
            "piid": 2,
            "access": ["read", "notify", "write"]
        },
        default=None
    )
    
    # piid: 3 (stop-time): (string, unit: None) (acc: ['read', 'notify', 'write'], value-list: [], value-range: None)
    dnd_stop_time: str = field(
        metadata={
            "siid": 5,
            "piid": 3,
            "access": ["read", "notify", "write"]
        },
        default=None
    )


    # siid 6: (map): 6 props, 2 actions
    # piid: 1 (map-data): (string, unit: None) (acc: ['notify'], value-list: [], value-range: None)
    map_data: str = field(
        metadata={
            "siid": 6,
            "piid": 1,
            "access": ["notify"]
        },
        default=None
    )
    
    # piid: 2 (frame-info): (string, unit: None) (acc: ['write'], value-list: [], value-range: None)
    frame_info: str = field(
        metadata={
            "siid": 6,
            "piid": 2,
            "access": ["write"]
        },
        default=None
    )

    # siid 7: (audio): 4 props, 2 actions
    # piid: 1 (volume): (int32, unit: None) (acc: ['read', 'notify', 'write'], value-list: [], value-range: [0, 100, 1])
    audio_volume: int = field(
        metadata={
            "siid": 7,
            "piid": 1,
            "access": ["read", "notify", "write"]
        },
        default=None
    )

    # piid: 2 (voice-packet-id): (string, unit: none) (acc: ['read', 'notify', 'write'], value-list: [], value-range: None)
    audio_language: str = field(
        metadata={
            "siid": 7,
            "piid": 2,
            "access": ["read", "notify", "write"]
        },
        default=None
    )

    # siid 8: (time): 3 props, 1 actions
    # piid: 1 (time-zone): (string, unit: None) (acc: ['read', 'notify'], value-list: [], value-range: None)
    timezone: str = field(
        metadata={
            "siid": 8,
            "piid": 1,
            "access": ["read", "notify"]
        },
        default=None
    )

    # siid 9: (Main Cleaning Brush): 2 props, 1 actions
    # piid: 1 (Brush Left Time): (uint16, unit: hour) (acc: ['read', 'notify'], value-list: [], value-range: [0, 300, 1])
    main_brush_left_time: int = field(
        metadata={
            "siid": 9,
            "piid": 1,
            "access": ["read", "notify"]
        },
        default=None
    )
    
    # piid: 2 (Brush Life Level): (uint8, unit: percentage) (acc: ['read', 'notify'], value-list: [], value-range: [0, 100, 1])
    main_brush_life_level: int = field(
        metadata={
            "siid": 9,
            "piid": 2,
            "access": ["read", "notify"]
        },
        default=None
    )

    # siid 10: (Side Cleaning Brush): 2 props, 1 actions
    # piid: 1 (Brush Left Time): (uint16, unit: hour) (acc: ['read', 'notify'], value-list: [], value-range: [0, 200, 1])
    side_brush_left_time: int = field(
        metadata={
            "siid": 10,
            "piid": 1,
            "access": ["read", "notify"]
        },
        default=None
    )
    
    # piid: 2 (Brush Life Level): (uint8, unit: percentage) (acc: ['read', 'notify'], value-list: [], value-range: [0, 100, 1])
    side_brush_life_level: int = field(
        metadata={
            "siid": 10,
            "piid": 2,
            "access": ["read", "notify"]
        },
        default=None
    )

    # siid 11: (Filter): 2 props, 1 actions
    # piid: 1 (Filter Life Level): (uint8, unit: percentage) (acc: ['read', 'notify'], value-list: [], value-range: [0, 100, 1])
    filter_life_level: int = field(
        metadata={
            "siid": 11,
            "piid": 1,
            "access": ["read", "notify"]
        },
        default=None
    )
    
    # piid: 2 (Filter Left Time): (uint16, unit: hour) (acc: ['read', 'notify'], value-list: [], value-range: [0, 150, 1])
    filter_left_time: int = field(
        metadata={
            "siid": 11,
            "piid": 2,
            "access": ["read", "notify"]
        },
        default=None
    )

    # siid 12: (clean-logs): 4 props, 0 actions
    # piid: 1 (first-clean-time): (uint32, unit: None) (acc: ['read', 'notify'], value-list: [], value-range: [0, 4294967295, 1])
    total_log_start: int = field(
        metadata={
            "siid": 12,
            "piid": 1,
            "access": ["read", "notify"]
        },
        default=None
    )
    
    # piid: 2 (total-clean-times): (uint32, unit: Minutes) (acc: ['read', 'notify'], value-list: [], value-range: [0, 4294967295, 1])
    total_clean_time: int = field(
        metadata={
            "siid": 12,
            "piid": 2,
            "access": ["read", "notify"]
        },
        default=None
    )
    
    # piid: 3 (total-clean-times): (uint32, unit: None) (acc: ['read', 'notify'], value-list: [], value-range: [0, 4294967295, 1])
    total_clean_count: int = field(
        metadata={
            "siid": 12,
            "piid": 3,
            "access": ["read", "notify"]
        },
        default=None
    )
    
    # piid: 4 (total-clean-area): (uint32, unit: None) (acc: ['read', 'notify'], value-list: [], value-range: [0, 4294967295, 1])
    total_area: int = field(
        metadata={
            "siid": 12,
            "piid": 4,
            "access": ["read", "notify"]
        },
        default=None
    )


class DreameVacuum(MiotDevice):
    """Support for dreame vacuum robot d9 (dreame.vacuum.p2009)."""

    _MAPPING = DreameStatus

    @command()
    def status(self) -> DreameStatus:
        return self.get_properties_for_dataclass(DreameStatus)

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

    @command()
    def set_fan_speed(self, speed):
        return self.set_property(fan_speed=speed)

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

    # siid ???: (Identify): 0 props, 1 actions
    # aiid ??? Identify: in: [] -> out: []
    @command()
    def find(self) -> None:
        """Find the robot."""
        return self.audio_position()  # Just play audio for now

    # siid 9: (Main Cleaning Brush): 2 props, 1 actions
    # aiid 1 Reset Brush Life: in: [] -> out: []
    @command()
    def reset_brush_life(self) -> None:
        """aiid 1 Reset Brush Life: in: [] -> out: []"""
        return self.call_action(9, 1)

    # siid 11: (Filter): 2 props, 1 actions
    # aiid 1 Reset Filter Life: in: [] -> out: []
    @command()
    def reset_filter_life(self) -> None:
        """aiid 1 Reset Filter Life: in: [] -> out: []"""
        return self.call_action(11, 1)

    # siid 10: (Side Cleaning Brush): 2 props, 1 actions
    # aiid 1 Reset Brush Life: in: [] -> out: []
    @command()
    def reset_brush_life2(self) -> None:
        """aiid 1 Reset Brush Life: in: [] -> out: []"""
        return self.call_action(10, 1)

    # siid 18: (clean): 16 props, 2 actions
    # aiid 1 开始清扫: in: [] -> out: []
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
    def room_id_cleanup(self, rooms, repeats,clean_mode,mop_mode) -> None:
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
            cleanlist.append([ ord(sublist[0].upper()) - 64, repeats, clean_mode, mop_mode, rooms.index(sublist) + 1 ])
        payload = [{"piid": 1, "value": 18}, {"piid": 10, "value": "{\"selects\": " + str(cleanlist).replace(' ','') + "}"  }]
        return self.call_action(4, 1, payload)

    @command(click.argument("coords", type=str))
    def restricted_zone(self, coords) -> None:
        """Create restricted/mop zone """
        payload = [{"piid": 4, "value": coords}]
        return self.call_action(6, 2, payload)

    @command()
    def manual_control_once(self, rotation, velocity) -> None:
        siid = 4
        piid = 15
        payload = [{
            "did": f"call-{siid}-{piid}",
            "siid": 4,
            "piid": 15,
            "value": "{\"spdv\": " + str(velocity) + ",\"spdw\": " + str(rotation) + ",\"audio\":\"false\",\"random\": " + str(randint(1000, 9999)) + "}"
        }]
        return self.send("set_properties", payload)

    # siid 6: (map): 6 props, 2 actions
    # aiid 1 map-req: in: [2] -> out: []
    @command()
    def map_req(self) -> None:
        """aiid 1 map-req: in: [2] -> out: []"""
        return self.call_action(6, 1)

    # aiid 2 set-map
    @command()
    def set_map(self, map_id) -> None:
        payload = [{"piid": 4, "value": "{\"sm\": " + "{" + "}" + ", \"mapid\":" + str(map_id) + "}"}]
        return self.call_action(6, 2, payload)

    @command(click.argument("water", type=int))
    def set_water_level(self, water):
        """Set water level"""
        return self.set_property(water_level=water)

    # siid 7: (audio): 4 props, 2 actions
    # aiid 1 : in: [] -> out: []
    @command()
    def audio_position(self) -> None:
        """TODO"""
        return self.call_action(7, 1)

    # aiid 2 : in: [] -> out: []
    @command()
    def install_voice_pack(self) -> None:
        """Install given voice pack."""
        payload = [{
            "did": "<myID>",
            "siid": 7,
            "piid": 4,
            "value": "{\"id\":\"EN\",\"url\":\"http://192.168.1.6:8123/local/dreame.vacuum.p2009_en.tar.gz\",\"md5\":\"d2287d7d125748bace8d0778b7df119c\",\"size\":1156119}"
        }]
        return self.send("set_properties", payload)

    # aiid 2 : in: [] -> out: []
    @command()
    def test_sound(self) -> None:
        """aiid 3 : in: [] -> out: []"""
        return self.call_action(7, 2)

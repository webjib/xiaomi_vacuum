from enum import IntEnum

DreameD9Mapping = {
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
    "property_carpet_boost": {"siid": 4, "piid": 12},
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
    "property_multi_map_enabled": {"siid": 6, "piid": 7},
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
    Strong = 2
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

from typing import Final
from .miio.dreame_const import (
    OperationStatus,
    VacuumStatus,
    VacuumSpeed,
    Waterbox,
    WaterLevel,
    OperatingMode,
    ErrorCodes,
)
from homeassistant.components.vacuum import (
    PLATFORM_SCHEMA,
    SUPPORT_STATE,
    SUPPORT_BATTERY,
    SUPPORT_LOCATE,
    SUPPORT_PAUSE,
    SUPPORT_RETURN_HOME,
    SUPPORT_START,
    SUPPORT_STOP,
    SUPPORT_FAN_SPEED,
    STATE_CLEANING,
    STATE_IDLE,
    STATE_PAUSED,
    STATE_RETURNING,
    STATE_DOCKED,
    STATE_ERROR,
    StateVacuumEntity,
)

DEFAULT_NAME: Final = "Xiaomi Vacuum cleaner"
DATA_KEY: Final = "vacuum.xiaomi_vacuum"

CONF_NO_SLEEP_DOCKED: Final = "no_sleep_when_docked"

ATTR_STATUS: Final = "status"
ATTR_ERROR: Final = "error"
ATTR_FAN_SPEED: Final = "fan_speed"
ATTR_CLEANING_TIME: Final = "cleaning_time"
ATTR_CLEANING_AREA: Final = "cleaning_area"
ATTR_MAIN_BRUSH_LEFT_TIME: Final = "main_brush_time_left"
ATTR_MAIN_BRUSH_LIFE_LEVEL: Final = "main_brush_life_percent"
ATTR_SIDE_BRUSH_LEFT_TIME: Final = "side_brush_time_left"
ATTR_SIDE_BRUSH_LIFE_LEVEL: Final = "side_brush_life_percent"
ATTR_FILTER_LIFE_LEVEL: Final = "filter_life_percent"
ATTR_FILTER_LEFT_TIME: Final = "filter_time_left"
ATTR_CLEANING_TOTAL_TIME: Final = "total_cleaning_time"
ATTR_CLEANING_TOTAL_COUNT: Final = "total_cleaning_count"
ATTR_CLEANING_TOTAL_AREA: Final = "total_cleaning_area"
ATTR_CLEANING_LOG_START: Final = "first_time_cleaning"
ATTR_WATERBOX_STATUS: Final = "waterbox"
ATTR_WATER_LEVEL: Final = "water_level"
ATTR_WATER_LEVEL_LIST: Final = "water_level_list"
ATTR_OPERATION_STATUS: Final = "operation_status"
ATTR_OPERATING_MODE: Final = "operating_mode"
ATTR_MAP_ID_LIST: Final = "map_id_list"
ATTR_ROOM_LIST: Final = "room_list"
ATTR_MULTI_MAP_ENABLED: Final = "multi_map_enabled"
ATTR_DND_ENABLED: Final = "dnd_enabled"
ATTR_DND_START_TIME: Final = "dnd_start"
ATTR_DND_STOP_TIME: Final = "dnd_stop"
ATTR_AUDIO_LANGUAGE: Final = "audio_language"
ATTR_AUDIO_VOLUME: Final = "audio_volume"
ATTR_TIMEZONE: Final = "timezone"
ATTR_CLEAN_CLOTH_TIP: Final = "clean_cloth_tip"
ATTR_SERIAL_NUMBER: Final = "serial_number"
ATTR_CARPET_BOOST: Final = "carpet_boost"

SERVICE_FAST_MAP: Final = "vacuum_fast_map"
SERVICE_SPOT_CLEAN: Final = "vacuum_spot_clean"
SERVICE_CLEAN_ZONE: Final = "vacuum_clean_zone"
SERVICE_CLEAN_ROOM_BY_ID: Final = "vacuum_clean_room_by_id"
SERVICE_SELECT_MAP: Final = "vacuum_select_map"
SERVICE_SET_RESTRICTED_ZONE: Final = "vacuum_set_restricted_zone"
SERVICE_RESET_FILTER_LIFE: Final = "vacuum_reset_filter_life"
SERVICE_RESET_MAIN_BRUSH_LIFE: Final = "vacuum_reset_main_brush_life"
SERVICE_RESET_SIDE_BRUSH_LIFE2: Final = "vacuum_reset_side_brush_life"
SERVICE_MOVE_REMOTE_CONTROL_STEP: Final = "vacuum_remote_control_move_step"
SERVICE_WATER_LEVEL: Final = "vacuum_set_water_level"
SERVICE_INSTALL_VOICE_PACK: Final = "vacuum_install_voice_pack"
SERVICE_SET_CLEAN_CLOTH_TIP: Final = "vacuum_set_clean_cloth_tip"
SERVICE_SET_AUDIO_VOLUME: Final = "vacuum_set_audio_volume"
SERVICE_DND: Final = "vacuum_do_not_disturb"
SERVICE_SET_CARPET_BOOST: Final = "vacuum_set_carpet_boost"
SERVICE_SET_MULTI_MAP: Final = "vacuum_set_multi_map"
SERVICE_RENAME_MAP: Final = "vacuum_rename_map"

INPUT_RC_ROTATION: Final = "rotation"
INPUT_RC_VELOCITY: Final = "velocity"
INPUT_MAP_ID: Final = "map_id"
INPUT_MAP_NAME: Final = "map_name"
INPUT_WALL_ARRAY: Final = "walls"
INPUT_ZONES_ARRAY: Final = "zones"
INPUT_MOP_ARRAY: Final = "mops"
INPUT_ZONE_ARRAY: Final = "zone"
INPUT_ZONE_REPEATER: Final = "repeats"
INPUT_ROOMS_ARRAY: Final = "rooms"
INPUT_CLEAN_MODE: Final = "clean_mode"
INPUT_MOP_MODE: Final = "mop_mode"
INPUT_LANGUAGE_ID: Final = "lang_id"
INPUT_DELAY: Final = "delay"
INPUT_URL: Final = "url"
INPUT_MD5: Final = "md5"
INPUT_SIZE: Final = "size"
INPUT_VOLUME: Final = "volume"
INPUT_DND_ENABLED: Final = "dnd_enabled"
INPUT_DND_START: Final = "dnd_start"
INPUT_DND_STOP: Final = "dnd_stop"
INPUT_CARPET_BOOST_ENABLED: Final = "carpet_boost_enabled"
INPUT_MULTI_MAP_ENABLED: Final = "multi_map_enabled"

STATE_MOPPING: Final = "mopping"
STATE_UNKNWON: Final = "unknown"

SPEED_SILENT: Final = "silent"
SPEED_STANDARD: Final = "standard"
SPEED_STRONG: Final = "strong"
SPEED_TURBO: Final = "turbo"

WATERBOX_PRESENT: Final = "present"
WATERBOX_REMOVED: Final = "removed"

WATER_LEVEL_LOW: Final = "low"
WATER_LEVEL_MEDIUM: Final = "medium"
WATER_LEVEL_HIGHT: Final = "high"

OPERATION_STATUS_COMPLETED: Final = "completed"
OPERATION_STATUS_AUTO_CLEAN: Final = "auto clean"
OPERATION_STATUS_CUSTOM_AREA_CLEAN: Final = "zone clean"
OPERATION_STATUS_AREA_CLEAN: Final = "room clean"
OPERATION_STATUS_SPOT_CLEAN: Final = "spot clean"
OPERATION_STATUS_FAST_MAPPING: Final = "fast mapping"

OPERATION_IDLE_MODE: Final = "idle"
OPERATION_PAUSE_AND_STOP_MODE: Final = "pause and stop"
OPERATION_AUTO_CLEAN_MODE: Final = "auto clean"
OPERATION_BACK_HOME_MODE: Final = "back home"
OPERATION_PART_CLEAN_MODE: Final = "part clean"
OPERATION_FOLLOW_WALL_MODE: Final = "follow wall"
OPERATION_CHARGING_MODE: Final = "charging"
OPERATION_OTA_MODE_MODE: Final = "ota mode"
OPERATION_FCT_MODE_MODE: Final = "fct mode"
OPERATION_WIFI_SET_MODE: Final = "wifi set"
OPERATION_POWER_OFF_MODE: Final = "power off"
OPERATION_FACTORY_MODE: Final = "factory"
OPERATION_ERR_REPOT_MODE: Final = "err repot"
OPERATION_REMOTE_CTRL_MODE: Final = "remote ctrl"
OPERATION_SLEEP_MODE: Final = "sleep"
OPERATION_SELF_TEST_MODE: Final = "self test"
OPERATION_FACTORY_FUNC_TEST: Final = "factory func test"
OPERATION_STANDBY_MODE: Final = "standby"
OPERATION_AREA_CLEAN: Final = "area clean"
OPERATION_CUSTOM_AREA_CLEAN: Final = "custom area clean"
OPERATION_SPOT_CLEAN: Final = "spot clean"
OPERATION_FAST_MAPPING: Final = "fast mapping"

ERROR_NO_ERROR: Final = "no error"
ERROR_DROP: Final = "drop"
ERROR_CLIFF: Final = "cliff"
ERROR_BUMPER: Final = "bumper"
ERROR_GESTURE: Final = "gesture"
ERROR_BUMPER_REPEAT: Final = "bumper repeat"
ERROR_DROP_REPEAT: Final = "drop repeat"
ERROR_OPTICAL_FLOW: Final = "optical flow"
ERROR_NO_BOX: Final = "no box"
ERROR_NO_TANKBOX: Final = "no tankbox"
ERROR_WATERBOX_EMPTY: Final = "waterbox empty"
ERROR_BOX_FULL: Final = "box full"
ERROR_BRUSH: Final = "brush"
ERROR_SIDE_BRUSH: Final = "side brush"
ERROR_FAN: Final = "fan"
ERROR_LEFT_WHEEL_MOTOR: Final = "left wheel motor"
ERROR_RIGHT_WHEEL_MOTOR: Final = "right wheel motor"
ERROR_TURN_SUFFOCATE: Final = "turn suffocate"
ERROR_FORWARD_SUFFOCATE: Final = "forward suffocate"
ERROR_CHARGER_GET: Final = "charger get"
ERROR_BATTERY_LOW: Final = "battery low"
ERROR_CHARGE_FAULT: Final = "charge fault"
ERROR_BATTERY_PERCENTAGE: Final = "battery percentage"
ERROR_HEART: Final = "heart"
ERROR_CAMERA_OCCLUSION: Final = "camera occlusion"
ERROR_CAMERA_FAULT: Final = "camera fault"
ERROR_EVENT_BATTERY: Final = "event battery"
ERROR_FORWARD_LOOKING: Final = "forward looking"
ERROR_GYROSCOPE: Final = "gyroscope"
ERROR_ROUTE_BLOCKED: Final = "route blocked"


SUPPORT_XIAOMI: Final = (
    SUPPORT_STATE
    | SUPPORT_BATTERY
    | SUPPORT_LOCATE
    | SUPPORT_RETURN_HOME
    | SUPPORT_START
    | SUPPORT_STOP
    | SUPPORT_PAUSE
    | SUPPORT_FAN_SPEED
)

STATE_CODE_TO_STATE: Final = {
    VacuumStatus.Unknown: STATE_UNKNWON,
    VacuumStatus.Sweeping: STATE_CLEANING,
    VacuumStatus.Idle: STATE_IDLE,
    VacuumStatus.Paused: STATE_PAUSED,
    VacuumStatus.Error: STATE_ERROR,
    VacuumStatus.Go_charging: STATE_RETURNING,
    VacuumStatus.Charging: STATE_DOCKED,
    VacuumStatus.Mopping: STATE_MOPPING,
}

SPEED_CODE_TO_NAME: Final = {
    VacuumSpeed.Unknown: STATE_UNKNWON,
    VacuumSpeed.Silent: SPEED_SILENT,
    VacuumSpeed.Standard: SPEED_STANDARD,
    VacuumSpeed.Strong: SPEED_STRONG,
    VacuumSpeed.Turbo: SPEED_TURBO,
}

WATERBOX_CODE_TO_NAME: Final = {
    Waterbox.Unknown: STATE_UNKNWON,
    Waterbox.Present: WATERBOX_PRESENT,
    Waterbox.Removed: WATERBOX_REMOVED,
}

WATER_CODE_TO_NAME: Final = {
    WaterLevel.Unknown: STATE_UNKNWON,
    WaterLevel.Low: WATER_LEVEL_LOW,
    WaterLevel.Medium: WATER_LEVEL_MEDIUM,
    WaterLevel.High: WATER_LEVEL_HIGHT,
}

OPERATION_STATUS_CODE_TO_NAME: Final = {
    OperationStatus.Unknown: STATE_UNKNWON,
    OperationStatus.OperationCompleted: OPERATION_STATUS_COMPLETED,
    OperationStatus.OperationAutoClean: OPERATION_STATUS_AUTO_CLEAN,
    OperationStatus.OperationCustomAreaClean: OPERATION_STATUS_CUSTOM_AREA_CLEAN,
    OperationStatus.OperationAreaClean: OPERATION_STATUS_AREA_CLEAN,
    OperationStatus.OperationSpotClean: OPERATION_STATUS_SPOT_CLEAN,
    OperationStatus.OperationFastMapping: OPERATION_STATUS_FAST_MAPPING,
}

OPERATING_MODE_CODE_TO_NAME: Final = {
    OperatingMode.Unknown: STATE_UNKNWON,
    OperatingMode.IdleMode: OPERATION_IDLE_MODE,
    OperatingMode.PauseAndStopMode: OPERATION_PAUSE_AND_STOP_MODE,
    OperatingMode.AutoCleanMode: OPERATION_AUTO_CLEAN_MODE,
    OperatingMode.BackHomeMode: OPERATION_BACK_HOME_MODE,
    OperatingMode.PartCleanMode: OPERATION_PART_CLEAN_MODE,
    OperatingMode.FollowWallMode: OPERATION_FOLLOW_WALL_MODE,
    OperatingMode.ChargingMode: OPERATION_CHARGING_MODE,
    OperatingMode.OtaModeMode: OPERATION_OTA_MODE_MODE,
    OperatingMode.FctModeMode: OPERATION_FCT_MODE_MODE,
    OperatingMode.WIFISetMode: OPERATION_WIFI_SET_MODE,
    OperatingMode.PowerOffMode: OPERATION_POWER_OFF_MODE,
    OperatingMode.FactoryMode: OPERATION_FACTORY_MODE,
    OperatingMode.ErrRepotMode: OPERATION_ERR_REPOT_MODE,
    OperatingMode.RemoteCtrlMode: OPERATION_REMOTE_CTRL_MODE,
    OperatingMode.SleepMode: OPERATION_SLEEP_MODE,
    OperatingMode.SelfTestMode: OPERATION_SELF_TEST_MODE,
    OperatingMode.FactoryFuncTest: OPERATION_FACTORY_FUNC_TEST,
    OperatingMode.StandbyMode: OPERATION_STANDBY_MODE,
    OperatingMode.AreaClean: OPERATION_AREA_CLEAN,
    OperatingMode.CustomAreaClean: OPERATION_CUSTOM_AREA_CLEAN,
    OperatingMode.SpotClean: OPERATION_SPOT_CLEAN,
    OperatingMode.FastMapping: OPERATION_FAST_MAPPING,
}

ERROR_CODE_TO_ERROR: Final = {
    ErrorCodes.Unknown: STATE_UNKNWON,
    ErrorCodes.NoError: ERROR_NO_ERROR,
    ErrorCodes.Drop: ERROR_DROP,
    ErrorCodes.Cliff: ERROR_CLIFF,
    ErrorCodes.Bumper: ERROR_BUMPER,
    ErrorCodes.Gesture: ERROR_GESTURE,
    ErrorCodes.Bumper_repeat: ERROR_BUMPER_REPEAT,
    ErrorCodes.Drop_repeat: ERROR_DROP_REPEAT,
    ErrorCodes.Optical_flow: ERROR_OPTICAL_FLOW,
    ErrorCodes.No_box: ERROR_NO_BOX,
    ErrorCodes.No_tankbox: ERROR_NO_TANKBOX,
    ErrorCodes.Waterbox_empty: ERROR_WATERBOX_EMPTY,
    ErrorCodes.Box_full: ERROR_BOX_FULL,
    ErrorCodes.Brush: ERROR_BRUSH,
    ErrorCodes.Side_brush: ERROR_SIDE_BRUSH,
    ErrorCodes.Fan: ERROR_FAN,
    ErrorCodes.Left_wheel_motor: ERROR_LEFT_WHEEL_MOTOR,
    ErrorCodes.Right_wheel_motor: ERROR_RIGHT_WHEEL_MOTOR,
    ErrorCodes.Turn_suffocate: ERROR_TURN_SUFFOCATE,
    ErrorCodes.Forward_suffocate: ERROR_FORWARD_SUFFOCATE,
    ErrorCodes.Charger_get: ERROR_CHARGER_GET,
    ErrorCodes.Battery_low: ERROR_BATTERY_LOW,
    ErrorCodes.Charge_fault: ERROR_CHARGE_FAULT,
    ErrorCodes.Battery_percentage: ERROR_BATTERY_PERCENTAGE,
    ErrorCodes.Heart: ERROR_HEART,
    ErrorCodes.Camera_occlusion: ERROR_CAMERA_OCCLUSION,
    ErrorCodes.Camera_fault: ERROR_CAMERA_FAULT,
    ErrorCodes.Event_battery: ERROR_EVENT_BATTERY,
    ErrorCodes.Forward_looking: ERROR_FORWARD_LOOKING,
    ErrorCodes.Gyroscope: ERROR_GYROSCOPE,
    ErrorCodes.RouteBlocked: ERROR_ROUTE_BLOCKED,
}

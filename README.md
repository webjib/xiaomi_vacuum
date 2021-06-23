# xiaomi_vacuum [WIP]
A custom component for Dreame Vacuum Robot D9 (dreame.vacuum.p2009).

Current list of attributes:
- fan_speed_list
- battery_level
- battery_icon
- fan_speed
- status
- waterbox
- operation_status
- operating_mode
- error
- dnd_enabled
- dnd_start
- dnd_stop
- audio_volume
- audio_language
- timezone
- main_brush_time_left
- side_brush_time_left
- filter_left_time
- cleaning_area
- cleaning_time
- first_time_cleaning
- total_cleaning_time
- total_cleaning_count
- total_cleaning_area
- water_level: high
- water_level_list
- map_id_list<sup>1</sup>
- room_list<sup>1</sup>

Current list of services:
- Xiaomi Vacuum: set_water_level
- Xiaomi Vacuum: vacuum_reset_filter_life
- Xiaomi Vacuum: vacuum_reset_main_brush_life
- Xiaomi Vacuum: vacuum_reset_side_brush_life
- Xiaomi Vacuum: set_map
- Xiaomi Vacuum: vacuum_clean_room_by_id<sup>1</sup>
- xiaomi Vacuum: Xiaomi Vacuum: vacuum_clean_zone
- ...

Note: To use features marked with <sup>1</sup>, you need to create a schedule in `MiHome` app, which you can disable (but do not remove).  
Select the rooms you want to be displayed in HA.  
Do not choose `All` when creating the cleaning schedule.  
Select rooms one by one, and afterwards this integration can get a list of your rooms.  


Using https://github.com/rytilahti/python-miio for the protocol.

Two possibilities for installation :
- Manually : add the "xiaomi_vacuum" folder to the /config/custom_components folder ; reboot
- With HACS : go in HACS, click on Integrations, click on the three little dots at top of the screen and selection "custom repositories", add this github url, select "Integration" as repository, and click ADD. Then go to the Integrations tab of HACS, and install the "Dreame Vacuum Robot D9" integration.

Code to add to configuration.yaml :
```
vacuum:
  - platform: xiaomi_vacuum
    host: <ip>
    token: "<token>"
    name: <name>
```
To retrieve the token, follow the default integration <a href="https://www.home-assistant.io/integrations/vacuum.xiaomi_miio/#retrieving-the-access-token">instructions</a>.

Works with https://github.com/denysdovhan/vacuum-card

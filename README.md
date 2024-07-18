Dependencies:
- ROS (tested in noetic)
- ttkbootstrap
`pip install ttkbootstrap`
- azure iot device
`pip install azure-iot-device`
- azure.iot.hub
`pip install azure-iot-hub`
- serial
`pip install pyserial`

TO-DO
- [x] 1. Make the button and label bigger (GUI) 
- [ ] 2. Define list of behavior and variables
- [ ] 3. Define list of experiments we can conduct
- [ ] 4. Evaluation matrix
- [ ] 5. Get the inspecting .. status from Taiwan side (robot movement + inspection)

Mapping
```
'0': {'label': "Unfinished", 'color': SECONDARY},
'1': {'label': "Robot Inspecting..", 'color': PRIMARY},
'2': {'label': "Accepted (Robot)", 'color': SUCCESS}, #based on inspection result >80%
'3': {'label': "Ask for help", 'color': WARNING}, #based on inspection result 60% - 80%
'4': {'label': "Rejected (Robot)", 'color': DANGER}, #based on inspection result <60%
'5': {'label': "Human Inspecting..", 'color': PRIMARY},
'6': {'label': "Inspected (Human)", 'color': SUCCESS}, #only inspecting, and inspected. Accepted or rejected can be decided manually by giving a mark
'9': {'label': "Robot going to ..", 'color': DARK} # next ssd that will be inspected by robot
```
To publish data using ROS
`rostopic pub --once /sub/aoi/spain/status std_msgs/String "data: '100000000000'"`





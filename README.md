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
- [ ] 6. Sync UI (Taiwan side)

Mapping
```
    '0': {'label': "Not Inspected", 'color': SECONDARY},
    '1': {'label': "H done - Good", 'color': SUCCESS},
    '2': {'label': "R done - Good", 'color': SUCCESS},
    '3': {'label': "H done - Bad", 'color': DANGER},
    '4': {'label': "R done - Bad", 'color': DANGER},
    '5': {'label': "H help", 'color': WARNING},
    '6': {'label': "R to do", 'color': DARK},
    '7': {'label': "Empty", 'color': LIGHT}
```
To publish data using ROS
```
rostopic pub --once /sub/aoi/spain/status std_msgs/String "data: '100000000000'"
```





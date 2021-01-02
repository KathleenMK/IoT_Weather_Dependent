### IoT_Weather_Dependent

# IOT Support of Depending on the Weather

*Networking using Connected Devices Assignment*

AIM

## Blynk App

pic

<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/image/Screenshot_blynk.jpg?raw=true" alt="BlynkScreenShot" width="250"/>
<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/Screenshot_blynk_off.jpg?raw=true" alt="BlynkScreenShotOff" width="250"/>

Beginning in the top left:
Notification widget: allows notifications to be pushed to the phone, in this case rain and nightfall will push a notification if at home
Email widget: allows emails to the sent, in this case rain and nightfall will send email if not at home
Webpage button: in this case met.ie for home location
Labelled value "Next Drying Window", using vertual pin V2, push reading rate, pushed from hardware at regular intervals
Labelled value: Followed By", using virtual pin V3, push reading rate, pushed from hardware
Button widget: "DRying", using virtual pin V5, switch mode
Labelled value: "Alerts", virtual pin V8, reading rate 15sec
Labelled value: "Current Conditions", virtual pin V4, reading rate 10sec
Labelled value: "School Drop 8am", virtual pin V10, pushed from hardware
Labelled value: "School Run 2PM", virtual pin V11, pushed from hardware
Labelled value: "Paint the Shed", virtual pin V12, pushed from hardware
GPS Stream: virtual pin V6, reads phone GPS location for use in home Indicator assignment


Blynk App "Depends on Weather" will display drying opportuinites forcast,

## Raspberry Pi

Interfaces with the Blynk app, runs the python script that interfaces with the Blynk app

### Web API
Provides the hourly local forcast that can be processed by a python sccript and resultant output

### Sensors

Rain Sensor Module:
Circuit details

Rain and hummidity sensors
Circuit details

### Python script
processes all the above and sends to Blynk


### Sense Hat
Displays current status, takes input for begining or ending the drying process



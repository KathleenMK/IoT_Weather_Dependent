### IoT_Weather_Dependent

# IOT Support of Depending on the Weather

*Networking using Connected Devices Assignment*

The aim of the project is to to define weather dependent “windows of opportunity”, get local weather forecast data, identify and take an action to make use of those opportunities.

### Blynk App
------------

<p>
<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/Screenshot_blynk.jpg?raw=true" alt="BlynkScreenShot" width="250"/>
<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/Screenshot_blynk_off.jpg?raw=true" alt="BlynkScreenShotOff" width="250"/>
Using the Blynk App virtual pins, the app displays the findings of a python script that runs on the raspberry pi!
There are two web page buttons, first in the top right to www.met.ie for the local weather forecast and secondly at the bottom of the screen to the ThingSpeak channel that shows the temperature, humidity and whether rain or drying was notified.
</p>

### Raspberry Pi
---------------

<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/pi.jpg" alt="BlynkScreenShotOff" width="250"/>

Interfaces with the Blynk app, runs the python script that interfaces with the Blynk app

#### Web API
Provides the hourly local forcast that can be processed by a python sccript and resultant output
https://prodapi.metweb.ie/weather/details/52.16235/-7.15244


#### Sensors

Rain Sensor Module Circuit details:
- AO, analog output, not connected 
- DO, digital output, connected to GPIO 18 (pin #12)
- GND, ground, connected to GND (pin #14)
- VCC connected to voltage 3V (pin #17)

Rain and hummidity sensor DHT11:
- Vcc+(+) connected to 5V (pin 4)
- GND(-) connected to GND (pin 6)
- Signal(out) connected to GPIO Pin 4 (pin 7)

#### Python script
Processes all the above and sends to Blynk

#### Sense Hat
Displays current status, takes input for begining or ending the drying process


### ThingSpeak Channel
---------------------
<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/thingspeak.png" alt="ThingSpeakCharts" width="350"/>
<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/thingtweet.png" alt="ThingTweet" width="350"/>

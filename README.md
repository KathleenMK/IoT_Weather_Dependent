### IoT_Weather_Dependent

# IOT Support of Depending on the Weather

*Networking using Connected Devices Assignment*

The aim of the project is to to define weather dependent “windows of opportunity”, get local weather forecast data, identify and take an action to make use of those opportunities.

### Blynk App
------------

<p>
<img align="right" src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/Screenshot_blynk.jpg?raw=true" alt="BlynkScreenShot" width="250"/>
<img align="right" src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/Screenshot_blynk_off.jpg?raw=true" alt="BlynkScreenShotOff" width="250"/>

Using the Blynk App virtual pins, the app displays the findings of a python script that runs on the raspberry pi!

- On the first row the notification and email widgets allow notifications to be pushed to the app and emails sent, in this case if it's raining or nightfall. The webpage button is linked to the local weather forcast on www.met.ie
- Virtual pins 2 and 3 display the day, time and duration of the next and following "drying window" calculated
- Virtual pin 5 is a button switch to indicate whether drying is taking place and therefore needs to be monitored for rain and nightfall
- Virtual pin 8 displays any current alerts
- Virtual pin 4 displays the actual local conditions
- Virtual pins 10, 11, 12 display other windows, in this case the next 8am and 2pm forecast for school runs and a drying window of greater than 6 hours
- Virtual pin 6 is the GPS stream widget, used to determine how far from home the phone is
- Lastly a web page button linking to the associated ThingSpeak channel
</p>   

   
### Raspberry Pi
---------------

Runs the python script [blynkRun.py](https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/blynkRun.py) that:
- requests forecast data from a web API
- interfaces with the virtual pins on the Blynk App
- takes input from rain and hummidity/temperature sensors
- takes input from the joystick on the Sense Hat and shows a simple display using the Sense Hat LEDs.

#### _Web API_

Data requested from a [public API](https://prodapi.metweb.ie/weather/details/52.16235/-7.15244)

#### _Sensors_

A CanaKit and four 10pin stacking headers was used to connect the sensors to the Raspberry Pi through the Sense Hat.

__Rain Sensor Module Circuit details:__
- AO, analog output, not connected 
- DO, digital output, connected to GPIO 18 (pin #12)
- GND, ground, connected to GND (pin #14)
- VCC connected to voltage 3V (pin #17)

<p>
<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/rainSensor_wiring.png" width="250"/>
  Image taken from: https://raspi.tv/2017/make-a-rain-alert-system-with-raspberry-pi
</p>

__Rain and hummidity sensor DHT11:__
- Vcc+(+) connected to 5V (pin 4)
- GND(-) connected to GND (pin 6)
- Signal(out) connected to GPIO Pin 4 (pin 7)

<p>
<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/dht11_wiring.png" width="250"/>
  Image taken from: https://www.thegeekpub.com/236867/using-the-dht11-temperature-sensor-with-the-raspberry-pi/
</p>
 
#### _Sense Hat_

Takes input from the joystick and shows a simple display using its LEDs.

### [ThingSpeak Channel](https://thingspeak.com/channels/1226853)
---------------------

<p>Displays the actual conditions as written to it from the python script on the Raspberry Pi.</p>
<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/thingspeak.png" alt="ThingSpeakCharts" width="350"/>

<p> Also includes a ThingTweet if drying is in progress and it's raining as a last resort to prompt action!</p>
<img src="https://github.com/KathleenMK/IoT_Weather_Dependent/blob/master/images/thingtweet.png" alt="ThingTweet" width="350"/>

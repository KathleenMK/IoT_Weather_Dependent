""" Main script required to interface with the BLYNK app "Depends on Weather"  
Purpose of script is to run the dryingWindowCalc.py script to identify drying windows,
    send that data to the Blynk app periodically
Also takes readings from a rain sensor to alert if rain is detected
Also takes readings from a hummidity/temperature sensor and sends current conditions to the Blynk app and ThingSpeak Channel
Determines what and when notifications are sent
displays on sense hat and takes input from the sensehat joystick
BLYNK authorisation code and home coordinates need to be populated on lines 66 and 236
"""

import requests   # https://www.w3schools.com/python/ref_requests_get.asp 28Nov20
import json
import blynklib
import Adafruit_DHT     # for use with the dht11 sensor
from sense_hat import SenseHat
import datetime
import time
from time import sleep
from gpiozero import InputDevice
import dryingWindowCalc #from dryingCalc import dryingWindows #https://stackoverflow.com/questions/36925670/calling-variables-in-another-module-python 08Dec20
import otherWindowCalc
#import presenceCheck
import haversine as hs #sudo pip3 install haversine 19Dec20 https://towardsdatascience.com/calculating-distance-between-two-geolocations-in-python-26ad3afe287b 17Dec20
import blynktimer
from urllib.request import urlopen  #required for sending to thingspeak

g=(0,50,0)
b=(0,0,0)
r=(50,0,0)
blue=(0,0,50)
greenAlt="#08FF08"
grey="#d3d3d3"
redAlt="#FF0000"

onPixels = [
    b, b, b, b, b, b, b, b,
    r, g, g, g, b, b, r, b,
    b, r, b, b, g, r, b, b,
    b, g, r, b, r, g, b, b,
    b, g, b, r, b, g, b, b,
    b, g, r, b, r, g, b, b,
    b, r, b, b, g, r, b, b,
    r, g, g, g, b, b, r, b
]

no_rain = InputDevice(18) #is true if not raining
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
sense = SenseHat()
sense.clear()
sense.show_message("On!", text_colour = blue)

""" Setting up the ThingSpeak channel write API key and the function that will write the actual data to it
"""
baseURL='https://api.thingspeak.com/update?api_key=JQDN71AM4HDX47C6' #% WRITE_API_KEY

def writeData(dry,humi,temp,rain,dryRain):
    # Sending the data to thingspeak in the query string
    conn = urlopen(baseURL + '&field5=%s&field6=%s&field7=%s&field8=%s&field1=%s' % (dry,humi,temp,rain,dryRain))
    print(conn.read())
    # Closing the connection
    conn.close()

""" Setting up the Blynk interface
"""
BLYNK_AUTH = ''     #Authorisation code required

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# create timers dispatcher instance
timer = blynktimer.Timer()

# message that prints to the terminal for timer events
WRITE_EVENT_PRINT_MSG = "[virtual_write] Pin: V{}, Value: '{}'"

"""
Upon the running of this script the drying is progress button (V5) is set to off
   and the remaining 7 virtual pins in use by the app are set to blank
   run_once is True and therefore not repeated
"""
@timer.register(vpin_num=5, interval=1, run_once=True)  # run at 1 sec, once only
def write_to_virtual_pin(vpin_num=1):
    value = 0 #off position
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, 0)
    
@timer.register(vpin_num=2, interval=1, run_once=True)
@timer.register(vpin_num=3, interval=1, run_once=True)
@timer.register(vpin_num=4, interval=1, run_once=True)
@timer.register(vpin_num=8, interval=1, run_once=True)
@timer.register(vpin_num=10, interval=1, run_once=True)
@timer.register(vpin_num=11, interval=1, run_once=True)
@timer.register(vpin_num=12, interval=1, run_once=True)
def write_to_virtual_pin(vpin_num=1):
    value = str(" ")
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, value)

""" Global variables to be used throughout
"""
global homeInd
homeInd = False #being set to False to demonstrate email notifications before being updated by the GPS stream

global drying
drying = False

global rain
rain = False

global nightInd
nightInd = None

global rainNotifyDue
rainNotifyDue = True

global nightNotifyDue
nightNotifyDue = True

#homeInd = len(presenceCheck.find_devices()) # no longer being used, replaced with GPS stream

""" Functions defined to be run in the while loop, along side the timer and Blynk runs
"""
# Function checks actual time to detemine whether it's night or not
def nightIndCheck():
    x=datetime.datetime.now()
    hour=int(x.strftime("%H"))
    global nightInd
    if hour >= 17:  #hardcoded for demo purposes
        nightInd = True
    else:
        nightInd = False

# Function, using rainNotifyDue indicator , determines if drying is in progress and if rain has been detected
# if so blynk notification sent to the app when phone is deemed home, otherwise an email is sent     
def notifyRain():
    global rainNotifyDue
    if drying and homeInd and rain and rainNotifyDue:
        blynk.notify("It's raining... clothes on the line!!!")
        rainNotifyDue = False
    elif drying and rain and rainNotifyDue:
        blynk.email('kathleenmcck@gmail.com', 'Its Raining', 'Please bring in the clothes') # could be multiple emails to all in the household
        rainNotifyDue = False
    elif not(drying and rain):
        rainNotifyDue = True    # notification set to True when drying status or rain status changes, stops repeated notifications being sent

# Function, using nightNotifyDue indicator , determines if drying is in progress and if it's night
# if so blynk notification sent to the app when phone is deemed home, otherwise an email is sent     
def notifyNight():
    global nightNotifyDue
    if drying and homeInd and nightInd and nightNotifyDue:
        blynk.notify("Its night! What about those clothes?")
        nightNotifyDue = False
    elif drying and nightInd and nightNotifyDue:
        blynk.email('kathleenmcck@gmail.com', 'Its Night time and the clothes are still out', 'Please bring in the clothes')
        nightNotifyDue = False
    elif not(drying and nightInd):
        nightNotifyDue = True   # notification set to True when drying status or night status changes

# Function to determine display on the sense hat
def senseHatDisplay():
    if drying and rain:
          sense.show_letter("R", text_colour = r)
    elif drying:
          sense.show_letter("D", text_colour = g)
    elif not drying:
        sense.set_pixels(onPixels)
    else:
        sense.show_letter("?", text_colour = r)


""" # Attempt to graph forcasted humidity for the next 24 hours using Blynk SuperChart 
# with humidity for the next 24 hours as the data stream assignment to virtual pin 17
# No longer being included as chart built for time as it passes not forcast
@timer.register(vpin_num=17, interval=20, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    dryingWindowCalc.calcDryingWindows()
    j=0
    while j < 24: 
        value=dryingWindowCalc.r[j]["humidity"]
        print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
        blynk.virtual_write(vpin_num, value)
        time.sleep(10)
        j=j+1
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, value) """


""" Functions defined to be run using the timer:
    Calculating the upcoming drying windows as calculated by dryingWindowCalc.py
    Writing to the virtual pins V2 (first entry of the dryingWindows array) and V3 (second entry, index 1, of the dryingWindows array)
    Web api seems to be updated hourly and so interval could be hourly, shorter interval for demo 
"""
@timer.register(vpin_num=2, interval=30, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    dryingWindowCalc.calcDryingWindows()
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    value = dryingWindowCalc.dryingWindows[0][0]+str(" @ ")+dryingWindowCalc.dryingWindows[0][1]+str(" for ")+str(dryingWindowCalc.dryingWindows[0][3])+str(" hours!")
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value)+str(currentTime))
    blynk.virtual_write(vpin_num, value)

@timer.register(vpin_num=3, interval=31, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    dryingWindowCalc.calcDryingWindows()
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    value = dryingWindowCalc.dryingWindows[1][0]+str(" @ ")+dryingWindowCalc.dryingWindows[1][1]+str(" for ")+str(dryingWindowCalc.dryingWindows[1][3])+str(" hours!")
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value)+str(currentTime))
    blynk.virtual_write(vpin_num, value)


""" Blynk Handle Write events, firstly the button (V5) to signify if drying is in progress, determines notifications,
    secondly the GPS stream (V6) used to determine if home
"""

@blynk.handle_event('write V5')
def write_virtual_pin_handler(pin, value):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    print('V5:'+ str(value)+str(currentTime))
    global drying  
    if value[0]=="1":
        drying=True
        print(str("drying is in progress, drying variable is ")+str(drying))
    else:
        drying=False
        print(str("drying not in progress, , drying variable is ")+str(drying))


# Phone location needs to be on for this event to engage, update interval 45 sec
@blynk.handle_event('write V6')
def write_virtual_pin_handler(pin, value):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    latitude = float(value[0])
    longitude = float(value[1])
    altitude = float(value[2])
    speed = float(value[3])
    home = (,)  #Home coordinates are required
    phone = (latitude,longitude)
    global distanceFromHome
    distanceFromHome = round(hs.haversine(home,phone),4) #measures distance in km
    global homeInd
    if distanceFromHome > 1:
        homeInd = False
    else:
        homeInd = True
    print('V6 Read: phone:'+str(phone)+' distanceFromHome:'+str(distanceFromHome)+' homeInd:'+str(homeInd))
               

""" Blynk Handle Read events, firstly the current conditions written to value display (V4) to signify if drying is in progress,
        within this event the current conditions are written to the ThingSpeak channel
    secondly the value display (V8) that shows any current rain or nightfall alerts when drying is in progress
"""
# reading rate 30sec
@blynk.handle_event('read V4')
def read_virtual_pin_handler(pin):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN) #https://www.thegeekpub.com/236867/using-the-dht11-temperature-sensor-with-the-raspberry-pi/ as at 03Dec20
    global rain
    global rainInd
    if not no_rain.is_active: ##https://raspi.tv/2017/make-a-rain-alert-system-with-raspberry-pi 02Dec20
       rain=True # should be True
       rainTxt="Rain"
       rainInd=1    
    else:
       rain=False
       rainTxt="Dry"
       rainInd=0
    current = ("Humidity:{1:0.0f}%, Temp:{0:0.0f}C, ".format(temperature, humidity)+str(rainTxt))
    print('V4 Read: '+str(current)+str(currentTime))
    blynk.virtual_write(pin, current)
    if drying:
        dryInd=1
    else:
        dryInd=0
    dryRain=dryInd*rainInd
    writeData(dryInd,humidity,temperature,rainInd,dryRain)
    print(dryInd,humidity,temperature,rainInd,dryRain)

# Blynk event that displays alerts if any and drying is in progress  
# reading rate 15sec
@blynk.handle_event('read V8')
def read_virtual_pin_handler(pin):
    blynk.set_property(pin, 'color', redAlt)
    print('V8 Read: rain:'+str(rain)+' nightInd:'+str(nightInd)+' drying:'+str(drying))
    if not(drying):
        blynk.virtual_write(pin, " ")
    elif drying and rain and nightInd:
        blynk.virtual_write(pin, "It's raining and Night time")
    elif drying and rain:
        blynk.virtual_write(pin, "It's raining")
    elif drying and nightInd:
        blynk.virtual_write(pin, "It's Night time")
    else:
        blynk.virtual_write(pin, "?")
    
""" Three additional write timer events to display the forcast for specific times/criteria
"""

# specific weekday hour, display the weather forecast
@timer.register(vpin_num=10, interval=62, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    otherWindowCalc.calcOtherWindows() #no account if data is not available... potential issue
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    value = otherWindowCalc.eightAM[0][1]+str(": ")+str(otherWindowCalc.eightAM[0][4])+str(" rainfall, ")+str(otherWindowCalc.eightAM[0][5])+str("C temp...")+str(otherWindowCalc.eightAM[0][6])
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value)+str(currentTime))
    blynk.virtual_write(vpin_num, value)
    if float(otherWindowCalc.eightAM[0][4]) == 0:
      blynk.set_property(vpin_num, 'color', greenAlt)
    else:
      blynk.set_property(vpin_num, 'color', redAlt)

# specific weekday hour, display the weather forecast
@timer.register(vpin_num=11, interval=63, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    otherWindowCalc.calcOtherWindows() #no account if data is not available... potential issue
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    value = otherWindowCalc.twoPM[0][1]+str(": ")+str(otherWindowCalc.twoPM[0][4])+str(" rainfall, ")+str(otherWindowCalc.twoPM[0][5])+str("C temp...")+str(otherWindowCalc.twoPM[0][6])
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value)+str(currentTime))
    blynk.virtual_write(vpin_num, value)
    if float(otherWindowCalc.twoPM[0][4]) == 0:
      blynk.set_property(vpin_num, 'color', greenAlt)
    else:
      blynk.set_property(vpin_num, 'color', redAlt)

# looking for more than 6 drying hours for specific task
@timer.register(vpin_num=12, interval=64, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    dryingWindowCalc.calcDryingWindows()
    #value = str("new calc") #random.randint(0, 20)
    for x in dryingWindowCalc.dryingWindows:
        value=str("nothing coming up...")
        blynk.set_property(vpin_num, 'color', grey)
        if x[3]>6:  #could also restrict the days to the weekend
            print(x)
            value=str(x[0])+str(", @ ")+str(x[1])+str("! You've ")+str(x[3])+str(" drying hours...")
            blynk.set_property(vpin_num, 'color', greenAlt)
            break
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, value)


""" While loop to run indefinitely
"""
while True:
    timer.run() #only works if there is a timer event repeating
    blynk.run()  
    nightIndCheck()
    notifyRain()
    notifyNight()
    senseHatDisplay()
    for event in sense.stick.get_events():
       print(event.direction, event.action)
       if event.action == "pressed":
           if drying:
            drying=False
            blynk.virtual_write(5, 0)
            blynk.virtual_write(15, 1)
            print(str("drying not in progress")+str(drying))
           else:
            drying=True
            blynk.virtual_write(5, 1)
            blynk.virtual_write(15, 1)
            print(str("drying in progress")+str(drying))           

""" Main script required to interface with the BLYNK app "Depends on Weather"  
Purpose of script is to run the dryingWindowCalc.py script to identify drying windows,
    send that data to the Blynk app periodically
Also takes readings from a rain sensor to alert if rain is detected
Also takes readings from a hummidity/temperature sensor and sends current conditions to the Blynk app
Determines what and when notifications are sent
displays on sense hat and takes input from the sensehat joystick
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
import dryingWindowCalc
import otherWindowCalc
#import presenceCheck
import haversine as hs #sudo pip3 install haversine 19Dec20 https://towardsdatascience.com/calculating-distance-between-two-geolocations-in-python-26ad3afe287b 17Dec20
import blynktimer
#import random

#from dryingCalc import dryingWindows #https://stackoverflow.com/questions/36925670/calling-variables-in-another-module-python 08Dec20
g=(0,255,0)
b=(0,0,0)
r=(255,0,0)

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
sense.show_message("On!", text_colour = (0,0,255))
sense.set_pixels(onPixels)
#homeInd = len(presenceCheck.find_devices())

BLYNK_AUTH = 'LTVERrZ1k3ghsbg-6wzZuZQRZWfwBbpS'

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# create timers dispatcher instance
timer = blynktimer.Timer()


WRITE_EVENT_PRINT_MSG = "[virtual_write] Pin: V{}, Value: '{}'"

# Upon the running if this script, setting drying button (V5) to OFF, using timer
    # using timer examples at https://github.com/blynkkk/lib-python/blob/master/examples/08_blynk_timer.py visited 28Dec20
@timer.register(vpin_num=5, interval=1, run_once=True)  # run at 1 sec, once only
def write_to_virtual_pin(vpin_num=1):
    value = 0 #off position
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, 0)

# When script is run, setting the virtual pin values on the Blynk app to be blank
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

global homeInd
homeInd = True

global drying
drying = False

global rain
rain = None

global nightInd
nightInd = None

global rainNotifyDue
rainNotifyDue = True

global nightNotifyDue
nightNotifyDue = True

def nightIndCheck():
    x=datetime.datetime.now()
    hour=int(x.strftime("%H"))
    global nightInd
    if hour >= 17:
        nightInd = True
    else:
        nightInd = False
    #print(hour)
    #print(nightInd)


def notifyRain():
    #print(str(drying)+str(homeInd)+str(rain))
    global rainNotifyDue
    if drying and homeInd and rain and rainNotifyDue:
        blynk.notify(rain)
        rainNotifyDue = False
    elif drying and rain and rainNotifyDue:
        blynk.email('kathleenmcck@gmail.com', 'Its Raining', 'Please bring in the clothes')
        rainNotifyDue = False
    elif not(drying and rain):
        rainNotifyDue = True

def notifyNight():
    #print(str(drying)+str(homeInd)+str(nightInd))
    global nightNotifyDue
    if drying and homeInd and nightInd and nightNotifyDue:
        blynk.notify("Its night! What about those clothes?")
        nightNotifyDue = False
    elif drying and nightInd and nightNotifyDue:
        blynk.email('kathleenmcck@gmail.com', 'Its Night time and the clothes are still out', 'Please bring in the clothes')
        print(nightNotifyDue)
        nightNotifyDue = False
        print(nightNotifyDue)
        print("in the notify night")
    elif not(drying and nightInd):
        nightNotifyDue = True



@timer.register(vpin_num=10, interval=62, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    otherWindowCalc.calcOtherWindows() #no account if data is not available... potential issue
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    value = otherWindowCalc.eightAM[0][1]+str(": ")+str(otherWindowCalc.eightAM[0][4])+str(" rainfall, ")+str(otherWindowCalc.eightAM[0][5])+str("C temp...")+str(otherWindowCalc.eightAM[0][6])
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value)+str(currentTime))
    blynk.virtual_write(vpin_num, value)
    if float(otherWindowCalc.eightAM[0][4]) == 0:
      blynk.set_property(vpin_num, 'color', '#08FF08')
    else:
      blynk.set_property(vpin_num, 'color', '#FF0000')

@timer.register(vpin_num=11, interval=63, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    otherWindowCalc.calcOtherWindows() #no account if data is not available... potential issue
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    value = otherWindowCalc.twoPM[0][1]+str(": ")+str(otherWindowCalc.twoPM[0][4])+str(" rainfall, ")+str(otherWindowCalc.twoPM[0][5])+str("C temp...")+str(otherWindowCalc.twoPM[0][6])
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value)+str(currentTime))
    blynk.virtual_write(vpin_num, value)
    if float(otherWindowCalc.twoPM[0][4]) == 0:
      blynk.set_property(vpin_num, 'color', '#08FF08')
    else:
      blynk.set_property(vpin_num, 'color', '#FF0000')


@timer.register(vpin_num=12, interval=64, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    value = str("new calc") #random.randint(0, 20)
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, value)



@timer.register(vpin_num=2, interval=60, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    dryingWindowCalc.calcDryingWindows()
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    value = dryingWindowCalc.dryingWindows[0][0]+str(" @ ")+dryingWindowCalc.dryingWindows[0][1]+str(" for ")+str(dryingWindowCalc.dryingWindows[0][3])+str(" hours!")
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value)+str(currentTime))
    blynk.virtual_write(vpin_num, value)



@timer.register(vpin_num=3, interval=61, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    dryingWindowCalc.calcDryingWindows()
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    value = dryingWindowCalc.dryingWindows[1][0]+str(" @ ")+dryingWindowCalc.dryingWindows[1][1]+str(" for ")+str(dryingWindowCalc.dryingWindows[1][3])+str(" hours!")
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value)+str(currentTime))
    blynk.virtual_write(vpin_num, value)





@blynk.handle_event('write V5')
def write_virtual_pin_handler(pin, value):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    print('V5:'+ str(value)+str(currentTime))
    global drying  #https://www.w3schools.com/python/python_variables_global.asp  03Dec20
    if value[0]=="1":
        drying=True
        print(str("drying is in progress, drying variable is ")+str(drying))
        sense.show_letter("D", text_colour = g)
    else:
        drying=False
        print(str("drying not in progress, , drying variable is ")+str(drying))
        sense.set_pixels(onPixels)
        

#https://www.thegeekpub.com/236867/using-the-dht11-temperature-sensor-with-the-raspberry-pi/ as at 03Dec20
@blynk.handle_event('read V4')
def read_virtual_pin_handler(pin):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    #humidity = str("Humidity: ")+str(round(sense.get_humidity(),2))+str("%")
    global rain
    if not no_rain.is_active: ##https://raspi.tv/2017/make-a-rain-alert-system-with-raspberry-pi 02Dec20
       rain=True # should be True
       rainTxt="Rain"
       blynk.set_property(pin, 'color', '#FF0000')      
    else:
       rain=False
       rainTxt="Dry"
       blynk.set_property(pin, 'color', '#23C48E')
    current = ("Humidity:{1:0.0f}%, Temp:{0:0.0f}C, ".format(temperature, humidity)+str(rainTxt))
    print('V4 Read: '+str(current)+str(currentTime))
    blynk.virtual_write(pin, current)


#phone location needs to be one for this event to engage
@blynk.handle_event('write V6')
def write_virtual_pin_handler(pin, value):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    latitude = float(value[0])
    longitude = float(value[1])
    altitude = float(value[2])
    speed = float(value[3])
    home = (52.1702,-7.15015)
    #phone = (52.1742080,-7.1585798)
    phone = (latitude,longitude)
    global distanceFromHome
    distanceFromHome = round(hs.haversine(home,phone),4)
    global homeInd
    if distanceFromHome > 1:
        homeInd = False
    else:
        homeInd = True
    print('V6 Read: phone:'+str(phone)+' distanceFromHome:'+str(distanceFromHome)+' homeInd:'+str(homeInd))
    

# Blynk event that displays following drying window on app    
@blynk.handle_event('read V8')
def read_virtual_pin_handler(pin):
    print('V8 Read: rain:'+str(rain)+' nightInd:'+str(nightInd))
    if not(drying):
        blynk.virtual_write(pin, " ")
    elif rain and nightInd:
        blynk.virtual_write(pin, "It's raining and Night time")
    elif rain:
        blynk.virtual_write(pin, "It's raining")
    elif nightInd:
        blynk.virtual_write(pin, "It's Night time")
    else:
        blynk.virtual_write(pin, " ")


while True:
    timer.run() #only works if there is a timer event repeating
    blynk.run()  
    nightIndCheck()
    notifyRain()
    notifyNight()
    for event in sense.stick.get_events():
       print(event.direction, event.action)
       if event.action == "pressed":
           if drying:
            drying=False
            blynk.virtual_write(5, 0)
            print(str("drying not in progress")+str(drying))
            sense.set_pixels(onPixels)
           else:
            drying=True
            blynk.virtual_write(5, 1)
            print(str("drying in progress")+str(drying))
            sense.show_letter("D", text_colour = g)
           

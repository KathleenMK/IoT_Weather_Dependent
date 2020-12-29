
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
#import presenceCheck
import haversine as hs #sudo pip3 install haversine 19Dec20 https://towardsdatascience.com/calculating-distance-between-two-geolocations-in-python-26ad3afe287b 17Dec20
import blynktimer
import random

#from dryingCalc import dryingWindows #https://stackoverflow.com/questions/36925670/calling-variables-in-another-module-python 08Dec20

no_rain = InputDevice(18) #is true if not raining
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
sense = SenseHat()
sense.clear()
sense.show_message("On!", text_colour = blue)
sense.show_letter("*", text_colour = blue)
#homeInd = len(presenceCheck.find_devices())


BLYNK_AUTH = 'LTVERrZ1k3ghsbg-6wzZuZQRZWfwBbpS'

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# create timers dispatcher instance
timer = blynktimer.Timer()

global homeInd
homeInd = True

global drying
drying = None

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
        blynk.notify("Its nightfall. what about those clothes?")
        nightNotifyDue = False
    elif drying and nightInd and nightNotifyDue:
        blynk.email('kathleenmcck@gmail.com', 'Its Nightfall and the clothes are still out', 'Please bring in the clothes')
        print(nightNotifyDue)
        nightNotifyDue = False
        print(nightNotifyDue)
        print("in the notify night")
    elif not(drying and nightInd):
        nightNotifyDue = True



WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_WRITE] Pin: V{} Value: '{}'"


@timer.register(vpin_num=5, interval=1, run_once=True)
def write_to_virtual_pin(vpin_num=1):
    value = 0 #HIGH #str(" ") #random.randint(0, 20)
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, 0)

#https://github.com/blynkkk/lib-python/blob/master/examples/08_blynk_timer.py 28Dec20
# Code below: register two timers for different pins with different intervals
# run_once flag allows to run timers once or periodically
@timer.register(vpin_num=2, interval=1, run_once=True)
@timer.register(vpin_num=3, interval=1, run_once=True)
@timer.register(vpin_num=4, interval=1, run_once=True)
@timer.register(vpin_num=8, interval=1, run_once=True)
@timer.register(vpin_num=10, interval=1, run_once=True)
@timer.register(vpin_num=11, interval=1, run_once=True)
@timer.register(vpin_num=12, interval=1, run_once=True)
def write_to_virtual_pin(vpin_num=1):
    value = str(" ") #random.randint(0, 20)
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, value)

@timer.register(vpin_num=10, interval=10, run_once=False)
@timer.register(vpin_num=11, interval=11, run_once=False)
@timer.register(vpin_num=12, interval=12, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    value = str("new calc") #random.randint(0, 20)
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, value)




@timer.register(vpin_num=3, interval=25, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    dryingWindowCalc.calcDryingWindows()
    value = dryingWindowCalc.dryingWindows[1][0]+str(" @ ")+dryingWindowCalc.dryingWindows[1][1]+str(" for ")+str(dryingWindowCalc.dryingWindows[1][3])+str(" hours!")
    #str("boomiest") #random.randint(0, 20)
    print(WRITE_EVENT_PRINT_MSG.format(vpin_num, value))
    blynk.virtual_write(vpin_num, value)


# Blynk event that displays next drying window on app
# V2 and V3 seems to work best when blynk reading rate is not equal
@blynk.handle_event('read V2')
def read_virtual_pin_handler(pin):
    dryingWindowCalc.calcDryingWindows()    #placed within handler so that it recalculates as Blynk is running
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    nextWindow=dryingWindowCalc.dryingWindows[0][0]+str(" @ ")+dryingWindowCalc.dryingWindows[0][1]+str(" for ")+str(dryingWindowCalc.dryingWindows[0][3])+str(" hours!") #int duration needed to be converted to str
    print('V2 Read: '+str(nextWindow)+str(currentTime))
    blynk.virtual_write(pin, nextWindow)
    
        
# Blynk event that displays following drying window on app    
@blynk.handle_event('read V3')
def read_virtual_pin_handler(pin):
    #dryingCalc.calcDryingWindows()
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    followingWindow=dryingWindowCalc.dryingWindows[1][0]+str(" @ ")+dryingWindowCalc.dryingWindows[1][1]+str(" for ")+str(dryingWindowCalc.dryingWindows[1][3])+str(" hours!")
    print('V3 Read: '+str(followingWindow)+str(currentTime)) 
    """ if(runCount==1):
        blynk.virtual_write(pin, " ")
        print('V3 runCount is '+str(runCount))
    else: """
    blynk.virtual_write(pin, followingWindow)
      


# does not engage until pressed on app
@blynk.handle_event('write V5')
def write_virtual_pin_handler(pin, value):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    print('V5:'+ str(value)+str(currentTime))
    global drying  #https://www.w3schools.com/python/python_variables_global.asp  03Dec20
    if value[0]=="1":
        drying=True
        print(str("drying is in progress")+str(drying))
        sense.show_letter("D", text_colour = green)
    else:
        drying=False
        print(str("drying not in progress")+str(drying))
        sense.show_letter("*", text_colour = blue)

#print(str(drying))
#https://raspi.tv/2017/make-a-rain-alert-system-with-raspberry-pi 02Dec20
#https://www.thegeekpub.com/236867/using-the-dht11-temperature-sensor-with-the-raspberry-pi/ as at 03Dec20
@blynk.handle_event('read V4')
def read_virtual_pin_handler(pin):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    #humidity = str("Humidity: ")+str(round(sense.get_humidity(),2))+str("%")
    global rain
    if not no_rain.is_active: #and drying==0: #so drying is not not in progress, so in progress
       rain=True # should be True
       """ if drying==True:
         blynk.set_property(pin, 'color', '#FF0000')
         sense.show_letter("R", text_colour = red)
         print(homeInd)
         if (homeInd):
             blynk.notify(rain)  #https://github.com/blynkkk/lib-python 01Dec20
         else:
             blynk.email('kathleenmcck@gmail.com', 'Its Raining', 'Please bring in the clothes')
       else:
         blynk.set_property(pin, 'color', '#C0C0C0')
         sense.show_letter("*", text_colour = blue)
         #sense.show_message("No Rain", text_colour = green) """
    else:
       rain=False
       """ if drying==1:
         blynk.set_property(pin, 'color', '#00FF00')
         sense.show_letter("D", text_colour = green)
       else:
         blynk.set_property(pin, 'color', '#C0C0C0')
         sense.show_letter("*", text_colour = blue) """
    #humidityR = ("Temp:{0:0.1f}C Humidity:{1:0.1f}%".format(temperature, humidity))+str(rain)
    humidityR = str("Humidity: ")+format(humidity)+str("%, ")+str(rain)  #seem to need format() for humidity when combined with str
    print('V4 Read: '+str(humidityR)+str(drying)+str(currentTime))
    blynk.virtual_write(pin, humidityR)


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
    distanceFromHome = hs.haversine(home,phone)
    global homeInd
    if distanceFromHome > 1:
        homeInd = False
    else:
        homeInd = True
    print(phone)
    print(distanceFromHome)
    print(homeInd)





# Blynk event that displays following drying window on app    
@blynk.handle_event('read V8')
def read_virtual_pin_handler(pin):
    #dryingCalc.calcDryingWindows()
    #currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    #followingWindow=dryingWindowCalc.dryingWindows[1][0]+str(" @ ")+dryingWindowCalc.dryingWindows[1][1]+str(" for ")+str(dryingWindowCalc.dryingWindows[1][3])+str(" hours!")
    print('V8 Read: '+str(rain)+str(nightInd))
    if not(drying):
        blynk.virtual_write(pin, " ")
    elif rain and nightInd:
        blynk.virtual_write(pin, "It's raining and Nighttime")
    elif rain:
        blynk.virtual_write(pin, "It's raining")
    elif nightInd:
        blynk.virtual_write(pin, "It's Nighttime")
    else:
        blynk.virtual_write(pin, " ")
        

while True:
    timer.run() #only works if there is a timer event repeating
    blynk.run()  
    nightIndCheck()
    notifyRain()
    notifyNight()
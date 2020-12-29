
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
#import blynktimer

#from dryingCalc import dryingWindows #https://stackoverflow.com/questions/36925670/calling-variables-in-another-module-python 08Dec20
#timer = blynktimer.Timer()
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
    if(runCount==1):
        blynk.virtual_write(pin, " ")
        print('V3 runCount is '+str(runCount))
    else:
        blynk.virtual_write(pin, followingWindow)
      


# does not engage until pressed on app
@blynk.handle_event('write V5')
def write_virtual_pin_handler(pin, value):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    print('V5:'+ str(value)+str(currentTime))
    global drying  #https://www.w3schools.com/python/python_variables_global.asp  03Dec20
    if value[0]=="1":
        drying=1
        print(str("drying is in progress")+str(drying))
    else:
        drying=0
        print(str("drying not in progress")+str(drying))

#print(str(drying))
#https://raspi.tv/2017/make-a-rain-alert-system-with-raspberry-pi 02Dec20
#https://www.thegeekpub.com/236867/using-the-dht11-temperature-sensor-with-the-raspberry-pi/ as at 03Dec20
@blynk.handle_event('read V4')
def read_virtual_pin_handler(pin):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    #humidity = str("Humidity: ")+str(round(sense.get_humidity(),2))+str("%")
    if not no_rain.is_active: #and drying==0: #so drying is not not in progress, so in progress
       rain="Rain Alert"
       if drying==1:
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
         #sense.show_message("No Rain", text_colour = green)
    else:
       rain="no rain"
       if drying==1:
         blynk.set_property(pin, 'color', '#00FF00')
         sense.show_letter("D", text_colour = green)
       else:
         blynk.set_property(pin, 'color', '#C0C0C0')
         sense.show_letter("*", text_colour = blue)
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
    if distanceFromHome > 0.01:
        homeInd = False
    else:
        homeInd = True
    print(phone)
    print(distanceFromHome)
        

while True:
    blynk.run()  


import requests   # https://www.w3schools.com/python/ref_requests_get.asp 28Nov20
import json
import blynklib
import Adafruit_DHT
import datetime
import time
from time import sleep
from gpiozero import InputDevice
import dryingCalc
from dryingCalc import dryingWindows #https://stackoverflow.com/questions/36925670/calling-variables-in-another-module-python 08Dec20

no_rain = InputDevice(18) #is true if not raining
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

BLYNK_AUTH = 'LTVERrZ1k3ghsbg-6wzZuZQRZWfwBbpS'

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# V2 and V3 seems to work best when blynk reading rate is not equal
@blynk.handle_event('read V2')
def read_virtual_pin_handler(pin):
    dryingCalc.calcDryingWindows()    #placed within handler so that it recalculates as Blynk is running
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    nextWindow=dryingCalc.dryingWindows[0][0]+str(" @ ")+dryingCalc.dryingWindows[0][1]+str(" for ")+str(dryingCalc.dryingWindows[0][3])+str(" hours!") #int duration needed to be converted to str
    print('V2 Read: '+str(nextWindow)+str(currentTime))
    blynk.virtual_write(pin, nextWindow)
    # blynk.notify('boo') #https://github.com/blynkkk/lib-python 01Dec20

@blynk.handle_event('read V3')
def read_virtual_pin_handler(pin):
    dryingCalc.calcDryingWindows()
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    followingWindow=dryingCalc.dryingWindows[1][0]+str(" @ ")+dryingCalc.dryingWindows[1][1]+str(" for ")+str(dryingCalc.dryingWindows[1][3])+str(" hours!")
    print('V3 Read: '+str(followingWindow)+str(currentTime)) 
    blynk.virtual_write(pin, followingWindow)

# does not engage until pressed on app, v4 not populated until it's pressed...
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



#https://raspi.tv/2017/make-a-rain-alert-system-with-raspberry-pi 02Dec20
#https://www.thegeekpub.com/236867/using-the-dht11-temperature-sensor-with-the-raspberry-pi/
# as at 03Dec20
@blynk.handle_event('read V4')
def read_virtual_pin_handler(pin):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    #humidity = str("Humidity: ")+str(round(sense.get_humidity(),2))+str("%")
    if not no_rain.is_active: #and drying==0: #so drying is not not in progress, so in progress
       rain="Rain Alert"
       if drying==1:
         blynk.notify(rain)
         blynk.set_property(pin, 'color', '#FF0000')
       else:
         blynk.set_property(pin, 'color', '#C0C0C0')
    else:
       rain="no rain"
       if drying==1:
         blynk.set_property(pin, 'color', '#00FF00')
       else:
         blynk.set_property(pin, 'color', '#C0C0C0')
    #humidityR = ("Temp:{0:0.1f}C Humidity:{1:0.1f}%".format(temperature, humidity))+str(rain)
    humidityR = str("Humidity: ")+format(humidity)+str("%, ")+str(rain)  #seem to need format() for humidity when combined with str
    print('V4 Read: '+str(humidityR)+str(drying)+str(currentTime))
    blynk.virtual_write(pin, humidityR)


# does not engage until pressed on app, v4 not populated until it's pressed...
@blynk.handle_event('write V6')
def write_virtual_pin_handler(pin, value):
    currentTime = datetime.datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
    print('V6:'+ str(value)+str(currentTime))
    #global drying  #https://www.w3schools.com/python/python_variables_global.asp  03Dec20
    if value[0]=="1":
        #drying=1
        print(str("value is 1, v6"))
    else:
        #drying=0
        print(str("value is not 1, v6"))



while True:
    blynk.run()

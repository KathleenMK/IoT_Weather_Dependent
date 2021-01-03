from urllib.request import urlopen
import  json
import  time
import dryingWindowCalc
from sense_hat import SenseHat

#WRITE_API_KEY='YOUR_CHANNEL KEY_FROM_THINGSPEAK'

baseURL='https://api.thingspeak.com/update?api_key=JQDN71AM4HDX47C6' #% WRITE_API_KEY

sense = SenseHat()

def writeData(hour,humi,rain):
    # Sending the data to thingspeak in the query string
    conn = urlopen(baseURL + '&field2=%s&field3=%s&field4=%s' % (hour,humi,rain))
    print(conn.read())
    # Closing the connection
    conn.close()

while True:
    dryingWindowCalc.calcDryingWindows()
    j=0
    while j < 24: 
        hour=dryingWindowCalc.r[j]["time"]
        humi=dryingWindowCalc.r[j]["humidity"]
        rain=dryingWindowCalc.r[j]["rainfall"]
        writeData(hour,humi,rain)
        time.sleep(20)
        j=j+1
    time.sleep(360)
        
"""
otherWindowCalc.py script

Defines the function calcotherWindows for use by blynkRun.py:
Step 1) gets the local weather forecast from public web api
Step 2) determines the conditions for the hours specified
"""

import requests   # https://www.w3schools.com/python/ref_requests_get.asp visited 28Nov20
import json

def calcOtherWindows():
 print("just begining the calculation of other windows")

# STEP 1: gets the local weather forecast from public web api
# ----------------------------------------------------------- 

# global URL, local weather forecast api taken from met.ie website 
 URL = 'https://prodapi.metweb.ie/weather/details/52.16235/-7.15244';

# sending get request and saving response as response object
 r = requests.get(url = URL).json() # r below is a python list, of length 97ish


# STEP 2: determines the conditions in the forecast for defined hours, 8am and 2pm
# -------------------------------------------------------------------------- 

 i=0
 global eightAM
 eightAM=[] #defining an empty array to be populated with hours that meet the drying criteria
 while i < len(r):  #while loop to check each entry in the above response "r"
      if r[i]["time"] == "08:00" and r[i]["shortDayName"] in ("Mon","Tue","Wed","Thu","Fri"): 
        eightAM.append(tuple((i,r[i]["day"],r[i]["time"],r[i]["temperature"],r[i]["rainfall"],r[i]["dayNumber"],r[i]["weatherDescription"])))
      i = i + 1

 i=0
 global twoPM
 twoPM=[] #defining an empty array to be populated with hours that meet the drying criteria
 while i < len(r):  #while loop to check each entry in the above response "r"
      if r[i]["time"] == "14:00" and r[i]["shortDayName"] in ("Mon","Tue","Wed","Thu","Fri"): 
        twoPM.append(tuple((i,r[i]["day"],r[i]["time"],r[i]["temperature"],r[i]["rainfall"],r[i]["dayNumber"],r[i]["weatherDescription"])))
      i = i + 1



#calcOtherWindows()
#print(eightAM)
#print(twoPM)



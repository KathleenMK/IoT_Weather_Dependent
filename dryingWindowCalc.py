"""
dryingWindowCalc.py script

Defines the function calcDryingWindows for use by blynkRun.py:
Step 1) gets the local weather forecast from public web api
Step 2) determines the hours in the forecast that meet the drying criteria
Step 3) assigns a window # if the hours are adjacent from the above step
Step 4) create and populate dryingWindows array with day, start time, day index and duration of window
"""

import requests   # https://www.w3schools.com/python/ref_requests_get.asp visited 28Nov20
import json

def calcDryingWindows():
 print("just begining the calculation of drying windows")

# STEP 1: gets the local weather forecast from public web api
# ----------------------------------------------------------- 

# global URL, local weather forecast api taken from met.ie website 
 URL = 'https://prodapi.metweb.ie/weather/details/52.16235/-7.15244';

# sending get request and saving response as response object
 global r
 r = requests.get(url = URL).json() # r below is a python list, of length 97ish


# STEP 2: determines the hours in the forecast that meet the drying criteria
# -------------------------------------------------------------------------- 
# rainfall zero
# humidity <= 90% (believe 70% is a better measure however using higher figure to show workings)
# time of day between 7am and 7pm
# json data being transformed into tuples (#https://www.w3schools.com/python/python_tuples.asp)
    #Tuples are used to store multiple items in a single variable.
    #A tuple is a collection which is ordered and unchangeable.
 i=0
 global dryingHours
 dryingHours=[] #defining an empty array to be populated with hours that meet the drying criteria
 while i < len(r):  #while loop to check each entry in the above response "r"
      if float(r[i]["rainfall"]) == 0 and float(r[i]["humidity"]) <= 95 and r[i]["time"] >= "07:00" and r[i]["time"] < "19:00" and int(r[i]["temperature"]) > 1: 
        dryingHours.append(tuple((i,r[i]["shortDayName"],r[i]["time"],r[i]["humidity"],r[i]["rainfall"],r[i]["dayNumber"])))
      i = i + 1


# STEP 3: Assigns a window # if the hours are adjacent from the above step
# ------------------------------------------------------------------------
# dyingHours array from above step being looped through to determine whether drying hours are adjacent using index from response object,
# if so deemed the same window and assigned the same window #
# windowcalc array defined and populated with drying hours and assigned window number as tuples
#def calcStepWindows():
 j=0
 windowNo=1
 global windowCalc
 windowCalc=[]
#data in later days is not per hour, but every 3 hours, therefore keeping the original r index to calculate the length of the window
 while j < len(dryingHours):
    if j == 0:
      windowCalc.append(tuple((dryingHours[j][0],dryingHours[j][1],dryingHours[j][2],dryingHours[j][5],windowNo)))
    else:
      if  dryingHours[j][0] == dryingHours[j-1][0]+1:
        windowCalc.append(tuple((dryingHours[j][0],dryingHours[j][1],dryingHours[j][2],dryingHours[j][5],windowNo)))
      else:
        windowNo = windowNo + 1
        windowCalc.append(tuple((dryingHours[j][0],dryingHours[j][1],dryingHours[j][2],dryingHours[j][5],windowNo)))
    j = j + 1



# STEP 4: Create and populate dryingWindows array with day, start time, day index and duration of window
# ------------------------------------------------------------------------------------------------------
# windowCalc above contains the following 5 pieces of data: 
# original list index; short day name; time; day number; window number 
# can't update a tuple, therefore only adding when all info known
 k=0
 global dryingWindows #make global to allow import into blynkRun file
 dryingWindows=[]
 while k < len(windowCalc):
    if k == 0:  #first window
      day=windowCalc[k][1]
      startTime=windowCalc[k][2]
      startHour=(startTime[0]+startTime[1]) #time always on the hour, taking the character at index 0 and 1
      dayNo=windowCalc[k][3]
    else:
      if windowCalc[k][4] != windowCalc[k-1][4]:   # window number is not the same as the previous
        # therefore previous window can be closed
        endTime=windowCalc[k-1][2]  # end time is taken from the previous entry
        endHour=(endTime[0]+endTime[1]) #time always on the hour, taking the character at index 0 and 1
        duration=(int(endHour)-int(startHour)+1) #duration is assuming 1 hour added to end hour
        dryingWindows.append(tuple((day,startTime,dayNo,duration))) # append complete window information to dryingWindows array
        # and new window processed (similar to where k is 0 above)
        day=windowCalc[k][1]
        startTime=windowCalc[k][2]
        startHour=(startTime[0]+startTime[1]) #time always on the hour, taking the character at index 0 and 1
        dayNo=windowCalc[k][3]
      if k == len(windowCalc)-1:  #last entry in the windowcalc array
            endTime=windowCalc[k][2]  #end assumed to be that of the last forcast, so 1 later than the last drying hour
            endHour=(endTime[0]+endTime[1]) 
            duration=(int(endHour)-int(startHour)+1)
            dryingWindows.append(tuple((day,startTime,dayNo,duration)))
    k = k + 1


#calcDryingWindows()
#print(len(dryingHours))
#print(dryingHours)
#print(len(windowCalc))
#print(windowCalc)
#print(dryingWindows)


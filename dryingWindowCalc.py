
import requests   # https://www.w3schools.com/python/ref_requests_get.asp 28Nov20
import json

def calcDryingWindows():
 print("just begining the calculation of drying windows")
# api
# global URL
 URL = 'https://prodapi.metweb.ie/weather/details/52.16235/-7.15244';
#sending get request and saving response as response object
# r below is a python list, of length 97ish
# global r 
 r = requests.get(url = URL).json()
 
#blynk.notify("boom")
#https://www.w3schools.com/python/python_tuples.asp
#Tuples are used to store multiple items in a single variable.
#A tuple is a collection which is ordered and unchangeable.
#def calcDryingHours():
 # getForecast()
 i=0
 dryingHours=[]
 while i < len(r):
      #print("in the dryingHours loop")
      if float(r[i]["rainfall"]) == 0 and float(r[i]["humidity"]) <= 95 and r[i]["time"] >= "07:00" and r[i]["time"] < "21:00": #expected to use humidity 70%, time 8 to 8
        dryingHours.append(tuple((i,r[i]["shortDayName"],r[i]["time"],r[i]["humidity"],r[i]["rainfall"],r[i]["dayNumber"])))
      i = i + 1
#def calcStepWindows():
 j=0
 windowNo=1
 windowCalc=[]
  #dryingWindows.append(tuple((0,dryingHours[0][0])))
  #data in later days is not per hour, but every 3 hours, what does that mean for the windows
  #therefore keeping the original r index to calculate the length of the window
 while j < len(dryingHours):
    #print("in the window calc step")
    if j == 0:
      windowCalc.append(tuple((dryingHours[j][0],dryingHours[j][1],dryingHours[j][2],dryingHours[j][5],windowNo)))
    else:
      if  dryingHours[j][0] == dryingHours[j-1][0]+1:
        windowCalc.append(tuple((dryingHours[j][0],dryingHours[j][1],dryingHours[j][2],dryingHours[j][5],windowNo)))
      else:
        windowNo = windowNo + 1
        windowCalc.append(tuple((dryingHours[j][0],dryingHours[j][1],dryingHours[j][2],dryingHours[j][5],windowNo)))
    j = j + 1
#so windowCalc list contains the following 5 pieces of data
# original list index
# short day name
# time
# day number
# window number
# would like to output time, day and number of hours in window
# can't update a tuple, only adding when all info known
#def calcDryingWindows():
  #getForecast()
 # calcDryingHours()
  #calcStepWindows()
 k=0
 global dryingWindows #make gloabl to aloow import into blynkData file
 dryingWindows=[]
 while k < len(windowCalc):
    #print("in the final calc step")
    if k == 0:
      day=windowCalc[k][1]
      startTime=windowCalc[k][2]
      startHour=(startTime[0]+startTime[1]) #time always on the hour, taking the character at index 0 and 1
      dayNo=windowCalc[k][3]
      #print(k)
      #dryingWindowSum.append(tuple((dryingWindows[k][1],dryingWindows[k][2],dryingWindows[k][3],dryingWindows[k][4],1))) #last value to be hours in window
    else:
      if windowCalc[k][4] != windowCalc[k-1][4]:   #so if the window number is the same as the previous
        endTime=windowCalc[k-1][2]  #end hour could reference the original list and check whether the interval is > 1
        endHour=(endTime[0]+endTime[1])
        #print(startHour)     
        #print(endHour)
        duration=(int(endHour)-int(startHour)+1)
        dryingWindows.append(tuple((day,startTime,dayNo,duration)))
        day=windowCalc[k][1]
        startTime=windowCalc[k][2]
        startHour=(startTime[0]+startTime[1]) #time always on the hour, taking the character at index 0 and 1
        dayNo=windowCalc[k][3]
        if k == len(windowCalc)-1:
            endTime=windowCalc[k][2]  #end assumed to be that of the last forcast, so 1 later than the last drying hour
            endHour=(endTime[0]+endTime[1]) 
            #print(startHour)     
            #print(endHour)
            duration=(int(endHour)-int(startHour)+1)
            dryingWindows.append(tuple((day,startTime,dayNo,duration))) #duration is incorrect as it hasn't been updated
            #print("the end")
    k = k + 1


calcDryingWindows()

 



#print(len(dryingHours))
#print(len(dryingWindows))

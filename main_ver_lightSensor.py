#!/usr/bin/env python

from login import login
import time
import grovepi

print("##### Lanch sensor program.... ####")

#-------------------------------------------------
# #### initialize sensor ####
print("setup all sensors...")
# Connect the Grove Light Sensor to analog port A0
light_sensor = 0
grovepi.pinMode(light_sensor,"INPUT")

print("finish sensors setup.")
#--------------------------------------------------
# ####initialize variables####
# input Value for event trigger
inputVal = 0
# statusFlag. default True
isAvailable = True
# cool time to trigger next  event
intervalTime = 5
# opearnd. When light strength is lower than this value, door is closed.
threshold_lightStrength = 100

#--------------------------------------------------
# #### login to salesforce ####
print("call logging function")
sf = login()
#--------------------------------------------------

print("#### Complete Lanching sensor program ####")

#--------------------------------------------------
# #### insert a record to initialize server status...
sf.CoffeeServerStatus__e.create({ 'DeviceName__c':'Sensor0001', 'isAvailable__c':isAvailable}) 

--------------------------------------------
print("start observation...")

while True:

    try:
        time.sleep(.5)

        # update input value
        inputVal = grovepi.analogRead(light_sensor)
        # print("brightness is " + str(inputVal))    
        
        # when 
        # 1. door closed and isAvailable OR
        # 2. door opened and isNotAvailable
        # then wait until status changed
        if (inputVal < threshold_lightStrength and isAvailable) or (inputVal > threshold_lightStrength and not(isAvailable)):
            continue
        
        # switching statusFlag
        print("!!!Status Changed!!!")
        print("    Updating caffeeServer status...")
        isAvailable = not(isAvailable)
        sf.CoffeeServerStatus__e.create({ 'DeviceName__c':'Sensor0001', 'isAvailable__c':isAvailable}) #insert
        print("    ....Complete updating.")
 
        print("---- Please wait " + str(intervalTime) + "sec...----")
        time.sleep(intervalTime)
        print("!!!Ready!!!")
        
    except KeyboardInterrupt:
        print("...stop observation.")
        break
    except IOError:
        print("IOError")
        break

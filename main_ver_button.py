#!/usr/bin/env python

from login import login
import time
import grovepi

print("##### Lanch sensor program.... ####")

#-------------------------------------------------
# #### initialize sensor ####
print("setup all sensors...")
# button plugged in D3
button = 3
grovepi.pinMode(button,"INPUT")
print("finish sensors setup.")
#--------------------------------------------------
# ####initialize variables####
# input Value for event trigger
inputVal = 0
# statusFlag. default false
isAvailable = False
# waitTime to enable event trigger
intervalTime = 5
#--------------------------------------------------
# #### login to salesforce ####
print("call logging function")
sf = login()
#--------------------------------------------------

print("#### Complete Lanching sensor program ####")

#--------------------------------------------------
print("start observation...")

while True:

    try:

        # update input value
        inputVal = grovepi.digitalRead(button)
        if inputVal == 1:
            # switching statusFlag
            print("!!!Event triggered!!!")
            print("    Updating caffeeserver status...")
            isAvailable = not(isAvailable)
            sf.CoffeeServerStatus__e.create({ 'DeviceName__c':'Sensor0001', 'isAvailable__c':isAvailable}) #insert
            print("    ....Complete updating.")
 
            print("---- Please wait " + str(intervalTime) + "sec...----")
            time.sleep(intervalTime)
            print("!!!Ready!!!")
        else:
            continue
            #nothing to do...
    except KeyboardInterrupt:
        print("...stop observation.")
        break
    except IOError:
        print ("Error")

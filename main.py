#!/usr/bin/env python

from login import login
from grovepi import *
from datetime import datetime
import time
import traceback
import sys

#-------------------------------------------------
# Declare static variable
LOG_DATETIME_FORMAT = "%Y%m%d_%H%M%S"
SIMPLE_SFDC_DICT_SUCCESS = "success"

print("##### Lanch sensor program.... ####")

#-------------------------------------------------
# #### initialize sensor ####
print("setup all sensors...")
# Connect the Grove Light Sensor to analog port A0
light_sensor = 0
pinMode(light_sensor,"INPUT")

# Connect the Grove LED(R,G,B) to Digital port D2,D3,D4
led_red = 7
led_blue = 8
pinMode(led_red, "OUTPUT")
pinMode(led_blue, "OUTPUT")

print("finish sensors setup.")
print("start showing program status via LED...")
# light led_red
digitalWrite(led_red, 1)

#--------------------------------------------------
# ####initialize variables####
# input Value for event trigger
inputVal = 0
# statusFlag. default True
isAvailable = True
# cool time to trigger next  event
intervalTime = 5
# opearnd. When light strength is lower than this value, door is closed.
threshold_lightStrength = 50

#--------------------------------------------------
# #### login to salesforce ####
print("call logging function")
sf = login()
#--------------------------------------------------

print("#### Complete Lanching sensor program ####")

#--------------------------------------------------
# #### insert a record to initialize server status...
sf.CoffeeServerStatus__e.create({ 'DeviceName__c':'Sensor0001', 'isAvailable__c':isAvailable}) 

#--------------------------------------------
# light led_blue and off led_green to show starting observation
digitalWrite(led_red, 0)
digitalWrite(led_blue, 1)

print("start observation...")

try :
	while True:

        	time.sleep(.5)

        	# update input value
        	inputVal = analogRead(light_sensor)
        	print("brightness is " + str(inputVal))

		# when light sensor detected unusual value(255), retry.
		if inputVal == 255:
			continue

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

       		# try request upto 3 times unless succeed
       		tryCount = 1
       		while tryCount < 4:
        		requestResult = sf.CoffeeServerStatus__e.create({ 'DeviceName__c':'Sensor0001', 'isAvailable__c':isAvailable}) #insert
        		if requestResult[SIMPLE_SFDC_DICT_SUCCESS]:
        	        	break
        		else:
        	        	print("    updating failed " + str(tryCount) + " time(s). retring...")
        	        	tryCount+=1

        	    	if tryCount > 3:
        	        	print("    Leached Re-Request limit. Raise Exception")
        	        	raise Exception("leached Re-Request limit. Last failed request result is -> " + str(requestResult))


	        print("    ....Complete updating.")

	        print("---- Please wait " + str(intervalTime) + "sec...----")
	        # start blink led_blue
	        digitalWrite(led_blue, 0)
	        totalWaitTime = 0
	        while totalWaitTime < intervalTime:
	        	time.sleep(0.5)
			digitalWrite(led_blue, 1)
	       		time.sleep(0.5)
	       		digitalWrite(led_blue, 0)
	         	totalWaitTime+=1

		#  switch LED color depended on server status.
		if isAvailable:
			digitalWrite(led_blue, 1)
			digitalWrite(led_red, 0)
		else:
			digitalWrite(led_blue, 0)
			digitalWrite(led_red, 1)

		print("!!!Ready!!!")

except KeyboardInterrupt:
	print("...stop observation.")
        # OFF all LEDs
        digitalWrite(led_red, 0)
        digitalWrite(led_blue, 0)

	sys.exit(0)
except:
        print("Exception Occured. Please Read log File.")
        with open("./log/error_" + datetime.now().strftime(LOG_DATETIME_FORMAT) + ".log",'a') as f:
        	traceback.print_exc(file=f)

        # light led_red to show ERROR
        digitalWrite(led_red, 1)
        digitalWrite(led_blue, 1)

	sys.exit(1)


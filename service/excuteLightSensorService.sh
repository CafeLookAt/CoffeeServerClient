#!/bin/sh

while :

do
	sudo python /home/pi/1_softwares/CoffeeServerClient/main.py >> Output.log
	statsuCode=$?

	if [ $statusCode = 0 ]; then
		break
	fi

done

#exit 0

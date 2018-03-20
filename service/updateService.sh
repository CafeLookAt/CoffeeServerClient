#!/bin/bash

sudo systemctl stop lightSensorService
sudo systemctl disable lightSensorService
sudo cp lightSensorService.service /etc/systemd/system
sudo systemctl enable lightSensorService

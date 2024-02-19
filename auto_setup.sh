#!/bin/bash

DIRECTORY=/opt/deck

if [ ! -d "$DIRECTORY" ]; then
    sudo mkdir /opt/deck
fi

env > enviroment

sudo cp ./main.py /opt/deck/main.py
sudo cp ./keybinds /opt/deck/keybinds
sudo cp ./listening_device /opt/deck/listening_device
sudo cp ./enviroment /opt/deck/enviroment

sudo cp ./deck.service /etc/systemd/system/deck.service

sudo systemctl daemon-reload

sudo systemctl enable deck.service --now

sudo systemctl restart deck.service

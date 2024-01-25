#!/bin/bash


id deck >> /dev/null

if [ $? != 0 ]; then
    echo "No service account found"
    sudo adduser --system --home /opt/deck --shell /bin/false --disabled-login --disabled-password --group deck
    sudo usermod -a -G deck $USER
    sudo usermod -a -G input deck
fi


sudo cp ./main.py /opt/deck/main.py
sudo cp ./main.py /opt/deck/keybinds
sudo cp ./main.py /opt/deck/listening_device

sudo cp ./deck.service /etc/systemd/system/deck.service

sudo systemctl daemon-reload

sudo systemctl enable deck.service --now

sudo systemctl restart deck.service

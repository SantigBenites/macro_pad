import os, pickle
from evdev import InputDevice, categorize, ecodes
CURRENTDIR = os.getcwd()


if os.path.exists(f"{CURRENTDIR}/keybinds"):
    with open(f'{CURRENTDIR}/keybinds', 'r') as fp: 
        key_bind_map = {}
        key_bind_entries = [line.rstrip().split(":") for line in fp]

        for entry in key_bind_entries:
            event, key, command = entry[0], entry[1], entry[2]

            if event not in key_bind_map.keys():
                key_bind_map[event] = {}
                
            key_bind_map[event][key] = command
else:
    key_bind_map = {}

# Keyboards to ignore .... all present in map 
device_list = []
for event_value in list(key_bind_map.keys()):
    dev = InputDevice('/dev/input/event0')
x = [dev.grab() for dev in device_list]

for event in dev.read_loop():
    
    # if key in map
    
    # Get from map[key] = key_value and commands

    # Execute commands

    # else ignore


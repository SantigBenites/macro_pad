import os, pickle
from evdev import InputDevice, categorize, ecodes
CURRENTDIR = os.getcwd()

# Keyboards to ignore .... all present in map 
dev = InputDevice('/dev/input/event0')
dev.grab()

if os.path.exists(f"{CURRENTDIR}/keybinds"):
    with open(f'{CURRENTDIR}/keybinds', 'r') as fp: 
        key_bind_map = {}
        
else:
    analysedFiles = {}

for event in dev.read_loop():
    
    # if key in map
    
    # Get from map[key] = key_value and commands

    # Execute commands

    # else ignore



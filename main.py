import os
from evdev import InputDevice, categorize, ecodes
# Keyboards to ignore .... all present in map 
dev = InputDevice('/dev/input/event0') 
dev.grab()

for event in dev.read_loop():
    
    # if key in map
    
    # Get from map[key] = key_value and commands

    # Execute commands

    # else ignore



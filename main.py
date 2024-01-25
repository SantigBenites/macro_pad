import os, pickle
from evdev import InputDevice, categorize, ecodes
CURRENT_DIR = os.getcwd()


if os.path.exists(f"{CURRENT_DIR}/keybinds"):
    with open(f'{CURRENT_DIR}/keybinds', 'r') as fp: 
        key_bind_map = {}
        key_bind_entries = [line.rstrip().split(":") for line in fp]

        for entry in key_bind_entries:
            key, command = entry[0], entry[1]                
            key_bind_map[key] = command
else:
    key_bind_map = {}

device_list = []
with open(f"{CURRENT_DIR}/listening_device","r") as listening_device_file:
    listening_device = listening_device_file.readline().strip()
    print(f"Listening from device {listening_device}")
    device = InputDevice(f'/dev/input/{listening_device}')
device.grab()

for event in device.read_loop():
    
    if event.type == ecodes.EV_KEY:
        key = categorize(event)
        if key.keystate == key.key_down:
            print("Event captured")
            key_code = key.keycode
            key_command = key_bind_map[key_code]
            os.system(key_command)


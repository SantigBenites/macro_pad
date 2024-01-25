import subprocess, re, os, sys, signal, evdev
#https://python-evdev.readthedocs.io/en/latest/
from evdev import InputDevice, categorize, ecodes
from utils import *
#https://pypi.org/project/sty/
from sty import fg, bg, ef, rs

from termios import tcflush, TCIFLUSH

CURRENT_DIR = os.getcwd() 

# xinput list
available_devices = subprocess.run("xinput list", 
                                    shell=True, 
                                    check=True, 
                                    capture_output = True, 
                                    text = True ).stdout.strip("\n")

print("Select device by ID")
print(available_devices)


available_indexes = re.findall('id=[0-9]*', available_devices)
available_indexes = [int(s[3:]) for s in available_indexes]
try:
    device_to_disable = int(input())
except ValueError:
    print("Not a valid number")
    exit(1)
    
device_to_disable_index = int(device_to_disable)
device_to_disable_name = subprocess.run(f"xinput list | grep 'id={device_to_disable_index}'", 
                                            shell=True, 
                                            check=True ,
                                            capture_output = True, 
                                            text = True ).stdout.strip("\n")
device_to_disable_name = device_to_disable_name.split("\t")[0].replace("↳","").strip()
    
if device_to_disable_index not in available_indexes:
    print("Not a valid device")
    exit(1)

# xinput --disable [id]
subprocess.run(f"xinput --disable {device_to_disable_index}", shell=True, check=True)

print(f"Disabled device with index {device_to_disable_index} \n")

# cat /proc/bus/input/devices
input_list = subprocess.run("cat /proc/bus/input/devices", 
                                    shell=True, 
                                    check=True, 
                                    capture_output = True, 
                                    text = True ).stdout.strip("\n")

p = re.compile('^.+-.+-.+$')
input_list = input_list.split("I:")
p = re.compile(f'{device_to_disable_name}')
device_string = [s for s in input_list if p.search(s)][0].strip('\n')

print(f"Device Information \n {device_string} \n")
event_value = re.findall('event[0-9]*', device_string)[0]

print(f"Device event stream is {event_value}")

with open(f"{CURRENT_DIR}/keybinds","a") as keybinds_file:
    try:
        # sudo actkbd -s -d /dev/input/[event]
        print("Press key to rebound \n")
        
        # cat /proc/bus/input/devices

        device = evdev.InputDevice(f'/dev/input/{event_value}')
        device.grab()
        key_code = "null"

        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key = categorize(event)
                if key.keystate == key.key_down:
                    key_code = key.keycode
                    device.close()
                    break

        print("Introduce command to use or leave blank and edit file keybinds\n")
        
        # Clearing the input buffer in the keyboard
        tcflush(sys.stdin, TCIFLUSH)
        command_for_selected_key = input()
        
        colored_event = fg.red + event_value + fg.rs
        colored_key_code = fg.red + key_code + fg.rs
        colored_command = fg.red + command_for_selected_key + fg.rs
        
        print(f"event is {colored_event} key is {colored_key_code} command is {colored_command}")
        
        with open(f"{CURRENT_DIR}/listening_device","r+") as listening_device:
            prev_listening_device = listening_device.readline().strip()
            if prev_listening_device != f"{device_to_disable_index}:{event_value}":
                print(f"Previosly read is {prev_listening_device} \nnew device is {device_to_disable_index}:{event_value}")
                print("Write yes to switch event device")
                if input().strip() == "yes":
                    listening_device.write(f"{device_to_disable_index}:{event_value}")
                
        
        print("Write yes to add keybind")
        
        if input().strip() == "yes":
            keybinds_file.write(f"{key_code}:{command_for_selected_key}\n")
            
    except KeyboardInterrupt:
        
        print("Finished binding")
        keybinds_file.close()
        sys.exit(0)
    

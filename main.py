import subprocess, re, os, sys

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
#subprocess.run(f"xinput --disable {device_to_disable_index}", shell=True, check=True)

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

CURRENT_DIR = os.getcwd() 

with open(f"{CURRENT_DIR}/keybinds") as keybinds_file:
    try:
        while True:
            # sudo actkbd -s -d /dev/input/[event]
            print("Press key to rebound \n")
            
            # cat /proc/bus/input/devices
            process = subprocess.Popen(f"sudo actkbd -s -d /dev/input/{event_value}", shell=True)
            process.wait()
            
            
    except KeyboardInterrupt:
        print("Finished binding")
        keybinds_file.close()
        sys.exit(0)
    

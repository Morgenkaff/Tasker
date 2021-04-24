#!/usr/bin/env python3

# IMPORTS:
import os, yaml, importlib

# VARS:
current_dir = None
config_file = None
watch_dir = None
threshold_val = None
counted_val = None

# SEPERATE FUNCTIONS:

def log(type, msg):
    
    # Casting any input to str (I thought this was python!?)
    msg = str(msg)
    
    if type == 1:
        print("INFO: " + msg)
        
    elif type == 2:
        print("WARNING: " + msg)
        
    elif type == 3:
        print("ERROR: " + msg)
        
    else: 
        print("WHAT!?")

# PRIMARY LOOP:

# Get configured values:

# get current dir for this file

current_dir = os.getcwd()

config_file = current_dir+"/config.yml"

# read conf.yaml-file and store in a dictionary (data)
f = open(config_file)
data = yaml.safe_load(f)

# set vars from values in config.json

# The directory to watch
watch_dir = data["watch_dir"]

# The threshhold value; the amount of files there should be, before taking action.
threshold_val = data["threshold_val"]


# Read amount of files in defined working_dir
counted_val = len([f for f in os.listdir(watch_dir) if os.path.isfile(os.path.join(watch_dir, f))])

# Compare to defined threshold_val

log(1, "watch_dir is: " + watch_dir)
log(1, "counted_val is: " + str(counted_val))
log(1, "threshold_val is: " + str(threshold_val))   

# if amount oifd files is higher than the given threshold create task
if counted_val > threshold_val:
    log(1, "Creating task")
# Else do nothing
else:
    # Busy doing nothing..
    log(1, "not creating task")


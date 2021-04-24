#!/usr/bin/env python3

# IMPORTS:
from datetime import datetime
import os, yaml, importlib, caldav


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
   
# Task creating function
def create_task():
    
    caldav_url = pers_data["url"]
    username = pers_data["username"]
    password = pers_data["password"]
    
    client = caldav.DAVClient(url=caldav_url, username=username, password=password)
    
    my_principal = client.principal()

    ## The principals calendars can be fetched like this:
    calendars = my_principal.calendars()
    if calendars:
        ## Some calendar servers will include all calendars you have
        ## access to in this list, and not only the calendars owned by
        ## this principal.
        print("your principal has %i calendars:" % len(calendars))
        for c in calendars:
            print("    Name: %-20s  URL: %s" % (c.name, c.url))
    else:
        print("your principal has no calendars")
    


# PRIMARY LOOP:

# Get configured values:

# get current dir for this file

current_dir = os.getcwd()

config_file = current_dir+"/config.yml"

pers_config_file = current_dir+"/pers_config.yml"

# read conf.yaml-file and store in a dictionary (data)
f = open(config_file)
data = yaml.safe_load(f)

pf = open(pers_config_file)
pers_data = yaml.safe_load(pf)

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
    
    create_task()
    
# Else do nothing
else:
    # Busy doing nothing..
    log(1, "not creating task")


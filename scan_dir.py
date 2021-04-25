#!/usr/bin/env python3

# IMPORTS:
import os, sys, yaml, caldav, datetime
from lxml import etree


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
        # Only print info if verbose flag is set
        if len(sys.argv) > 1:
            if sys.argv[1] == "-v":
                print("INFO: " + msg)
    
    elif type == 2:
        print("WARNING: " + msg)
        
    elif type == 3:
        print("ERROR: " + msg)
        
    else: 
        print("WHAT!?")
   
# Task creating function
def create_task():
    
    # Create the string with the neede values for the VTODO
    # The values that can/should be changed are:
    # PRODID - The name of this scripts/"products" author/coorporation
    # UID - A unique ID (to seperate the task from other tasks)
    # DTSTAMP - Date stamp in the format yyyymmddThhmmssZ
    # SUMMARY - Name for the task
    # CATEGORIES - Which categories the task should be tagged with
    # PRIORITY - Default priority (1 is highest, 9 is lowest, 0 is off)
    #
    # The rest of the properties are/should be (sure?) static
    
    # The prod_id is for now just the author of this script..
    prod_id = "Morgenkaff"
    
    # Because I wan't to use the date and time in the unique id
    # I get the date and time (the "now")
    now = datetime.datetime.now()
    
    # Creating a unique id by using the date+time and the prod_id
    # In the format yyyymmddThhmmss-prod_id
    unique_id = now.strftime('%Y%m%dT%H%M%S-') + prod_id
    
    # Creating the date stamp from the "now" too
    date_stamp = now.strftime('%Y%m%dT%H%M%SZ')
    
    # The name for the tasks is taken from the conf.yml file
    summary = data["name"]
    
    # The category/tag (there could be more) is set to 'Bot'.
    # I use this for when sorting my tasks, to see if any 
    # automatically created tasks exists.
    # (This usually means cleanup tasks - yay!)
    categories = "Bot"
    
    # The priority is taken from the conf.yml file
    priority = data["priority"]
    
    # The resulting string is created as an f string.
    # Simply because it is a messy string, and some
    # "new lines" help reading it, but we still need to
    # embed the created string vars from above.
    calendar.add_todo(f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:{prod_id}
BEGIN:VTODO
UID:{unique_id}
DTSTAMP:{date_stamp}
SUMMARY: {summary}
CATEGORIES:{categories}
STATUS:NEEDS-ACTION
PRIORITY:{priority}
END:VTODO
END:VCALENDAR""")    
    
    # Just printing todos (testing)
    #todos = calendar.todos()
    #print(todos[0].data)
    
    #print(todos[1].data)
    
    


# PRIMARY LOOP:

# Get configured values:

# get current dir for this file

current_dir = os.environ['HOME']

config_file = current_dir+"/.config/tasker/config.yml"

pers_config_file = current_dir+"/pers_config.yml"

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

# if amount of files is higher than the given threshold create task
# (if it does not exists already)
if counted_val > threshold_val:
    log(1, "It's time to clean up in the directopry. Connecting to the task list.")
    
    # Set the nescessary vars to connect to the server
    caldav_url = data["url"]
    username = data["username"]
    password = data["password"]
    
    # Screating the client
    client = caldav.DAVClient(url=caldav_url, username=username, password=password)
    
    # Setting the calendar (The one the new task should be created in)
    calendar = client.calendar(url=caldav_url)

    # Get the todo list. Gives an list type
    todos = calendar.todos()
    
    # Set a var to store if the tasks already exists or not
    task_exist = 0
    
    # Traverse the list, to see if there already is a task,
    # with the name given from the config.yml file
    for x in range(len(todos)):
        #print(todos[x].data)
        if data["name"] in todos[x].data:
            task_exist = 1
            break
        
            
            
    if task_exist:
        log(1, "Task exist. So not going to create one.")
    else:
        log(1, "Task does not exist. So going to create it.")
        
        # If not, create it:
        create_task()
        
        log(1, "Task created.")
    
# Else do nothing
else:
    # Busy doing nothing..
    log(1, "not creating task")


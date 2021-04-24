from datetime import datetime
import sys

## We'll try to use the local caldav library, not the system-installed
sys.path.insert(0, '..')
sys.path.insert(0, '.')

import caldav

## DO NOT name your file calendar.py or caldav.py!  We've had several
## issues filed, things break because the wrong files are imported.
## It's not a bug with the caldav library per se.

## CONFIGURATION.  Edit here, or set up something in
## tests/conf_private.py (see tests/conf_private.py.EXAMPLE).
caldav_url = 'https://nextcloud.georgcenter.duckdns.org/remote.php/dav'
username = 'emil'
password = 'Z6emX-i5WWZ-bmYmd-sLi57-W6nEk'

## When using the caldav library, one should always start off with initiating a
## DAVClient object, which should contain connection details and credentials.
## Initiating the object does not cause any requests to the server, so this
## will not break even if caldav url is set to example.com
client = caldav.DAVClient(url=caldav_url, username=username, password=password)

## For the convenience, if things are correctly set up in test config,
## the code below may replace the client object with one that works.
#if 'example.com' in caldav_url and password == 'Z6emX-i5WWZ-bmYmd-sLi57-W6nEk':
    #from tests.conf import client as client_
    #client = client_()

## Typically the next step is to fetch a principal object.
## This will cause communication with the server.
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
    
    ## Let's try to find or create a calendar ...
try:
    ## This will raise a NotFoundError if calendar does not exist
    my_new_calendar = my_principal.calendar(name="Test calendar")
    assert(my_new_calendar)
    ## calendar did exist, probably it was made on an earlier run
    ## of this script
except caldav.error.NotFoundError:
    ## Let's create a calendar
    my_new_calendar = my_principal.make_calendar(name="Test calendar")

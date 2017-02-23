# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
__author__ = "Haoyu (Chris) Lin"
__copyright__ = "Copyright 2017"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Haoyu (Chris) Lin"
__email__ = "haoyul3@student.unimelb.edu.au"

__description__ = "This script uses `GMail for Python`
                (git://github.com/charlierguo/gmail.git) module to read
                your UoM account and try to book in automatically when 
                there is event place available."
"""

import getpass
import json
import base64
import re
import urllib2
import time
import gmail

mode = input('1. type the student email and pwd directly;\n2. use the config file to save the effort of typing everytime (less secure!)\nchoose \'1\' or \'2\' and then press the ENTER key:')

if mode == 1:
        stu_login_name = raw_input('\nstudent login name (\"@student.unimelb.edu.au\" not needed):')
        password = getpass.getpass('password:')
        sleep_time = input('sleep time (sec):')
elif mode == 2:    
    # read the config
    with open('config.json') as json_file:
        config = json.load(json_file)
        stu_login_name = config[u'stu_login_name']
        password = config[u'password']
        sleep_time = config[u'sleep_time']
else:
    print "please choose \'1\'or \'2\'"
    exit(0)

username = stu_login_name+"@student.unimelb.edu.au"
sleep_time = float(sleep_time)

# log in
g = gmail.login(username, password)
if g.logged_in:
    print "\nlog in successfully.\n"

while True:
    # read possible mals
    psb_mails = g.inbox().mail(unread=True,sender="careers-online@unimelb.edu.au")
    for psb_mail in psb_mails:
        psb_mail.fetch()
        if "event places now available for booking" in psb_mail.subject:
            content = base64.b64decode(psb_mail.body)
            # print content
            # use regexp to get the url to book in
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
            # print urls
            for url in urls:
                if "ViewEvent" in url:
                    event_id = url.split("=")[1]
                    # print event_id
                    event_url = "https://careersonline.unimelb.edu.au/ViewEvent.chpx?id="+event_id
                    position = content.find(event_url)
                    print content[position:].split(">")[1].split("<")[0]
                if "emailbook" in url:
                    book_url = url
                    # open the url
                    response = urllib2.urlopen(url)
                    result = response.read()
                    if "You have successfully booked in" in result:
                        print "You have successfully booked in to this event!"
                    elif "Invalid Link" in result:
                        print "You have already booked in to this event."
                    else:
                        print "You are late."
            psb_mail.read()
    print "\nsleeping for " + str(sleep_time) + " second(s)\n"
    time.sleep(sleep_time)

# log out
g.logout()
print "\nlogged out."
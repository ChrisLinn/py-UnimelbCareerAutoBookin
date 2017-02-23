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


import json
import base64
import re
import urllib2
import gmail

# read the config
with open('config.json') as json_file:
    config = json.load(json_file)

# log in
g = gmail.login(config[u'username'], config[u'password'])
if g.logged_in:
    print "log in successfully.\n"

# read possible mals
psb_mails = g.inbox().mail(unread=True,sender="careers-online@unimelb.edu.au")
for psb_mail in psb_mails:
    content = psb_mail.fetch()
    try:
        content = base64.b64decode(psb_mail.body)
        # use regexp to get the url to book in
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        for url in urls:
            if "emailbook" in url:
                # open the url
                response = urllib2.urlopen(url)
                result = response.read()
                if "You have successfully booked in" in result:
                    print "You have successfully booked in!"
                elif "Invalid Link" in result:
                    print "You have already booked in."
                else:
                    print "You are late."
    except (TypeError):
        pass

# log out
g.logout()
print "\nlogged out."
# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
__author__ = "Haoyu (Chris) Lin"
__copyright__ = "Copyright 2017, The UoM_CareerAutoBookIn Project"
__credits__ = ["Charlie Guo"]

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Haoyu (Chris) Lin"
__email__ = "haoyul3@student.unimelb.edu.au"

Description:    This script using `GMail for Python`
                (git://github.com/charlierguo/gmail.git) module to reads your
                UoM account and try to book in automatically when there is
                event place available. 
"""


import json
import base64
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
    content = base64.b64decode(psb_mail.body)
    print content
    # parse the content and get to url to book in
    # open the url

# log out
g.logout()
print "logged out."
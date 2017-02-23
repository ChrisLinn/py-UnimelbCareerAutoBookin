# -*- coding: utf-8 -*-
#!/usr/bin/env pytho

"""
__author__ = "Chris Lin"
__copyright__ = "Copyright 2017, The UoM_CareerAutoBookIn Project"
__credits__ = ["Charlie Guo"]

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Chris Lin"
__email__ = "haoyul3@student.unimelb.edu.au"

Description:    This script using `GMail for Python`
                (git://github.com/charlierguo/gmail.git) module to reads your
                UoM account and try to book in automatically when there is
                event place available. 
"""

import gmail 

g = gmail.login(username, password)

if g.logged_in:
    print "login successfully!"
g.logout()
####################################3
# Maim Program for sending sms.
# CopyRight: I got the base code from ineternet and did some modification to make it work
# Date: 31/1/2014
# Author : Dipankar
####################################


#!/usr/bin/python
import sys
import time
from   urlparse import urlparse,parse_qs
import re
from   time import sleep
import traceback
from ConfigParser import ConfigParser
import pdb
import cookielib
import urllib2

import way2sms
import one6tiby2

try:
    from optparse import OptionParser
except ImportError:
    print "Error importing optparse module"
    sys.exit(1)

import pdb
default_service = '160by2'

#post wait time in seconds, depends on connection speed.
post_wait = 3

#Turn on debug to get additional information
debug = False

#Useragent:
user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)"

dump_file = "/tmp/160by2.debug.html"


def main():
    parser = OptionParser()
    usage = "Usage: %prog -s [server] -m [number] -t [text]"
    parser = OptionParser(usage=usage, version="%prog 1.0")
    parser.add_option("-m", "--number",  action="store", type="string",dest="number",  help="Mobile number to send sms")
    parser.add_option("-t", "--text", action="store", type="string", dest="text", help="Text to send")
    parser.add_option("-s", "--server", action="store", type="string", dest="server", help="use 160by2 or way2sms")
    (options, args) = parser.parse_args()

    #Read Credentials
    default_service = "way2sms"
    if options.server and options.server in ['160by2','way2sms']:
        default_service = options.server
    config = ConfigParser()
    config.read("../config.ini")
    username = config.get(default_service, "uname")
    password = config.get(default_service, "password")
    
    if options.number and options.text:
       text = options.text +' '+ ' '.join(args)
       if default_service == 'way2sms':
         handler = way2sms.smsHandler(username,password)
       else:
         handler = one6tiby2.smsHandler(username,password)
       handler.do(options.number,text)
    elif len(args) >1:
       num =args[0]
       text = ' '.join(args[1:])
       if default_service == 'way2sms':
         handler = way2sms.smsHandler(username,password)
       else:
         handler = one6tiby2.smsHandler(username,password)
       handler.do(num,text)

    else:
       print "Fatal: Required arguments are missing!"
       print "It's so simple to use : "
       print "1. sms.py 8147830733 Hi I am Dipankar"
       print "2. sms.py -s 160by2 8147830733 Hi! Dipankar again !"
       print "3. sms.py -s way2sms -m 8147830733 -t Yes ! Dipankar Again"
       print "Use: -h / --help to get help."

if __name__ == "__main__":
   main()

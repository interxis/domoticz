#!/usr/bin/python
#   Title: check_device_online.py
#   Author: Chopper_Rob
#   Date: 27-10-2014
#   Info: Checks the presence of the given device on the network and reports back to domoticz
#   URL : https://www.chopperrob.nl/domoticz/5-report-devices-online-status-to-domoticz
#   Version : 1.4
 
import sys
import datetime
import time
import os
import subprocess
import urllib2
import json
import base64
 
# Settings for the domoticz server
domoticzserver="192.168.1.5:8080"
domoticzusername = "alexis"
domoticzpassword = "L@L!mon@de"
 
# DO NOT CHANGE BEYOND THIS LINE
if len(sys.argv) != 5 :
  print ("Not enough parameters. Needs %Host %Switchid %Interval %Cooldownperiod.")
  sys.exit(0)
 
device=sys.argv[1]
switchid=sys.argv[2]
interval=sys.argv[3]
cooldownperiod=sys.argv[4]
previousstate=-1
lastsuccess=datetime.datetime.now()
lastreported=-1
base64string = base64.encodestring('%s:%s' % (domoticzusername, domoticzpassword)).replace('\n', '')
domoticzurl = 'http://'+domoticzserver+'/json.htm?type=devices&filter=all&used=true&order=Name'
 
if int(subprocess.check_output('ps x | grep \'' + sys.argv[0] + ' ' + sys.argv[1] + '\' | grep -cv grep', shell=True)) > 2 :
 print (datetime.datetime.now().strftime("%H:%M:%S") + "- script already running. exiting.")
 sys.exit(0)
 
def domoticzstatus ():
  json_object = json.loads(domoticzrequest(domoticzurl))
  if json_object["status"] == "OK":
    for i, v in enumerate(json_object["result"]):
      if json_object["result"][i]["idx"] == switchid and "Lighting" in json_object["result"][i]["Type"] :
        if json_object["result"][i]["Status"] == "On": 
          status = 1
        if json_object["result"][i]["Status"] == "Off": 
          status = 0
  return status
 
def domoticzrequest (url):
  request = urllib2.Request(url)
  request.add_header("Authorization", "Basic %s" % base64string)
  response = urllib2.urlopen(request)
  return response.read()
 
print (datetime.datetime.now().strftime("%H:%M:%S") + "- script started.")
 
 
 
lastreported = domoticzstatus()
if lastreported == 1 :
  print (datetime.datetime.now().strftime("%H:%M:%S") + "- according to domoticz, " + device + " is online")
if lastreported == 0 :
  print (datetime.datetime.now().strftime("%H:%M:%S") + "- according to domoticz, " + device + " is offline")
 
while 1==1:
  currentstate = subprocess.call('ping -q -c1 -W 1 '+ device + ' > /dev/null', shell=True)
 
  if currentstate == 0 : lastsuccess=datetime.datetime.now()
  if currentstate == 0 and currentstate != previousstate and lastreported == 1 : 
    print (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " online, no need to tell domoticz")
  if currentstate == 0 and currentstate != previousstate and lastreported != 1 :
    if domoticzstatus() == 0 :
      print (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " online, tell domoticz it's back")
      domoticzrequest("http://" + domoticzserver + "/json.htm?type=command&param=switchlight&idx=" + switchid + "&switchcmd=On&level=0")
    else:
      print (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " online, but domoticz already knew")
    lastreported=1
 
  if currentstate == 1 and currentstate != previousstate :
    print (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " offline, waiting for it to come back")
 
  if currentstate == 1 and (datetime.datetime.now()-lastsuccess).total_seconds() > float(cooldownperiod) and lastreported != 0 :
    if domoticzstatus() == 1 :
      print (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " offline, tell domoticz it's gone")
      domoticzrequest("http://" + domoticzserver + "/json.htm?type=command&param=switchlight&idx=" + switchid + "&switchcmd=Off&level=0")
    else:
      print (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " offline, but domoticz already knew")
    lastreported=0
 
  time.sleep (float(interval))
 
  previousstate=currentstate



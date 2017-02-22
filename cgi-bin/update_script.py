#!/usr/bin/python
import paho.mqtt.client as mqtt
import cgi  
import MySQLdb
import sys
import json

from db_conf import *

request=json.loads(cgi.FieldStorage().value)
poeid=request['poeid']
poemode=request['poemode']
poetext=request['poetext']

connect = MySQLdb.connect(host = db_host, user = db_user, passwd = db_passwd, db = db_name,)
cursor = connect.cursor()
cursor.execute("UPDATE Script SET Text='%s' WHERE ID='%s' AND Mode=%d"%(poetext, poeid, poemode)) 
cursor.execute("SELECT Mode FROM State WHERE ID='%s'"%(poeid))
row = cursor.fetchone()
isPublish = False
if (row[0]==1 or row[0]==2) and (poemode==3 or poemode==4):
  isPublish = True
cursor.execute("UPDATE State SET Mode=%d WHERE ID='%s'"%(poemode, poeid))
cursor.close()
connect.commit()
connect.close()      

if isPublish:
  client = mqtt.Client()
  # client.connect("47.88.195.145", 61613, 60)
  client.connect("127.0.0.1", 1883, 60)
  client.loop_start()
  client.publish("/timepoint", json.dumps({"device_key":poeid}))
  client.loop_stop()
  client.disconnect()

print 'content-type: application/json\n\n'
print json.dumps({})

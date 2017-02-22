#!/usr/bin/python
import cgi  
import MySQLdb
import sys
import json

from db_conf import *

request=json.loads(cgi.FieldStorage().value)
poeid=request['poeid']
settings=request['settings']

connect = MySQLdb.connect(host = db_host, user = db_user, passwd = db_passwd, db = db_name,)
cursor = connect.cursor()
cursor.execute("DELETE FROM Mode3 WHERE ID='%s'"%(poeid))
for setting in settings:  
  cursor.execute("INSERT INTO Mode3 VALUES('%s', '%s', %d, '%s', %d, '%s') "% (poeid, setting['OutputID'], int(setting['OutputValue']), setting['InputID'], int(setting['InputValue']), setting['DelayTime']))

poetxt='import datetime\n'
poetxt+='now = datetime.datetime.now()\n'
poetxt+='\n'
cursor.execute("SELECT * FROM Mode3 WHERE ID='%s'"%(poeid))
rows = cursor.fetchall()
for row in rows:  
  str = 'if I%s==%d and (now-T%s).seconds>=%d:\n'%(row[3], row[4], row[3], row[5].seconds)
  str += '  O%s=%s\n'%(row[1], row[2])
  poetxt += str
cursor.execute("INSERT INTO Script VALUES ('%s',3,'%s') ON DUPLICATE KEY UPDATE Text='%s'"%(poeid, poetxt, poetxt))
cursor.close()
connect.commit()
connect.close()      

print 'content-type: application/json\n\n'
print json.dumps({'text':poetxt})

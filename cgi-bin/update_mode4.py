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
cursor.execute("DELETE FROM Mode4 WHERE ID='%s'"%(poeid))
for setting in settings:  
  cursor.execute("INSERT INTO Mode4 VALUES('%s', '%s', %d, '%s', '%s') "% (poeid, setting['OutputID'], int(setting['OutputValue']), setting['StartTime'], setting['EndTime']))

poetxt='import datetime\n'
poetxt+='now = datetime.datetime.now()\n'
poetxt+='seconds=now.second+now.minute*60+now.hour*3600\n'
poetxt+='\n'
cursor.execute("SELECT * FROM Mode4 WHERE ID='%s'"%(poeid))
rows = cursor.fetchall()
for row in rows:  
  str = 'if %s<=seconds and seconds<=%s :\n'%(row[3].seconds, row[4].seconds)
  str += '  O%s=%s\n'%(row[1], row[2])
  poetxt += str

cursor.execute("INSERT INTO Script VALUES ('%s',4,'%s') ON DUPLICATE KEY UPDATE Text='%s'"%(poeid, poetxt, poetxt))
cursor.close()
connect.commit()
connect.close()      

print 'content-type: application/json\n\n'
print json.dumps({'text':poetxt})

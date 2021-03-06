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
cursor.execute("DELETE FROM Mode1 WHERE ID='%s'"%(poeid))
for setting in settings:  
  cursor.execute("INSERT INTO Mode1 VALUES ('%s', '%s', %d, '%s', %d)"%(poeid, setting['OutputID'], int(setting['OutputValue']), setting['InputID'], int(setting['InputValue'])))

poetxt=''
cursor.execute("SELECT * FROM Mode1 WHERE ID='%s'"%(poeid))
rows = cursor.fetchall()
for row in rows:  
  str = 'if I%s==%d:\n'%(row[3], row[4])
  str += '  O%s=%d\n'%(row[1], row[2])
  poetxt += str  
cursor.execute("INSERT INTO Script VALUES ('%s',1,'%s') ON DUPLICATE KEY UPDATE Text='%s'"%(poeid, poetxt, poetxt))
cursor.close()
connect.commit()
connect.close()      

print 'content-type: application/json\n\n'
print json.dumps({'text':poetxt})

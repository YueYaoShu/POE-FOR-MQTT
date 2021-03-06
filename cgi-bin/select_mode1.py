#!/usr/bin/python
import cgi  
import MySQLdb
import sys
import json

from db_conf import *

request=json.loads(cgi.FieldStorage().value)
poeid=request['poeid']

connect = MySQLdb.connect(host = db_host, user = db_user, passwd = db_passwd, db = db_name,)
cursor = connect.cursor()
cursor.execute("SELECT * FROM Mode1 WHERE ID='%s'"%(poeid))
rows = cursor.fetchall()
cursor.close()
connect.close()    

items = []
for row in rows:  
  item = {} 
  item['OutputID'] = row[1]  
  item['OutputValue'] = row[2]  
  item['InputID'] = row[3]  
  item['InputValue'] = row[4]   
  items.append(item)  
  
print 'content-type: application/json\n\n'
print json.dumps(items)

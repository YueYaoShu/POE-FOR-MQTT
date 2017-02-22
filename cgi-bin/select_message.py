#!/usr/bin/python
import cgi  
import MySQLdb
import sys
import json

from db_conf import *

request=json.loads(cgi.FieldStorage().value)
pageno=request['pageno']

connect = MySQLdb.connect(host = db_host, user = db_user, passwd = db_passwd, db = db_name,)
cursor = connect.cursor()
cursor.execute("SELECT * FROM Message ORDER BY Stamp DESC LIMIT %d, 10"%((pageno-1)*10))
rows = cursor.fetchall()
cursor.close()
connect.close()        

items = []
for row in rows:  
  item = {} 
  item['ID'] = row[0]  
  item['Content'] = row[1]
  item['Stamp'] = row[2].strftime('%Y-%m-%d %H:%M:%S')
  items.append(item)
 
print 'content-type: application/json\n\n'
print json.dumps(items)

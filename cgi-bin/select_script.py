#!/usr/bin/python
import cgi  
import MySQLdb
import sys
import json

from db_conf import *

request=json.loads(cgi.FieldStorage().value)
poeid=request['poeid']
poemode=request['poemode']

connect = MySQLdb.connect(host = db_host, user = db_user, passwd = db_passwd, db = db_name,)
cursor = connect.cursor()
cursor.execute("SELECT * FROM Script WHERE ID='%s' AND Mode=%d"% (poeid, poemode))
row = cursor.fetchone()
cursor.close()
connect.close()        

item = {} 
item['poeid'] = row[0]  
item['poemode'] = row[1]
item['poetext'] = row[2]
 
print 'content-type: application/json\n\n'
print json.dumps(item)

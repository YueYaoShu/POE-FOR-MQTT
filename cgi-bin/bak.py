#!/usr/bin/python
import cgi  
import MySQLdb
import sys
import json

db_host = 'localhost'
db_user = 'root'
db_passwd = 'mysql'
db_name = 'mqtt'

request=json.loads(cgi.FieldStorage().value)
poeid=request['poeid']


conn = MySQLdb.connect(host = db_host, user = db_user, passwd = db_passwd, db = db_name,)
cur = conn.cursor()
sql = "SELECT * FROM mode1 WHERE id='%s'"% (poeid)
cur.execute(sql)
data = cur.fetchall()

jsondata = {'txt':'', 'settings':[]}

for row in data:  
  item = {} 
  item['outputid'] = row[1]  
  item['outputvalue'] = row[2]  
  item['inputid'] = row[3]  
  item['inputvalue'] = row[4]   
  jsondata['settings'].append(item)  
  
sql = "SELECT txt FROM script WHERE mode=1 AND id='%s'"% (poeid)
cur.execute(sql)
data = cur.fetchone()
jsondata['txt'] = data[0]
cur.close()
conn.close()      
  
  
print 'Content-Type: application/json\n\n'
print json.dumps(jsondata)

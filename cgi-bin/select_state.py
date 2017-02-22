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
cursor.execute("SELECT * FROM State WHERE id='%s'"% (poeid))
row = cursor.fetchone()
cursor.close()
connect.close()        

item = {} 
i=0
item['ID'] = row[i]
i+=1
item['Mode'] = row[i]
i+=1
item['Stamp'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['V113101'] = row[i]
i+=1
item['V113102'] = row[i]
i+=1
item['V113103'] = row[i]
i+=1
item['V113104'] = row[i]
i+=1
item['V113105'] = row[i]
i+=1
item['V113106'] = row[i]
i+=1
item['V113107'] = row[i]
i+=1
item['V113108'] = row[i]
i+=1
item['V115101'] = row[i]
i+=1
item['V115102'] = row[i]
i+=1
item['V115103'] = row[i]
i+=1
item['V115104'] = row[i]
i+=1
item['V115105'] = row[i]
i+=1
item['V115106'] = row[i]
i+=1
item['V115107'] = row[i]
i+=1
item['V115108'] = row[i]
i+=1
item['V111101'] = row[i]
i+=1
item['V111102'] = row[i]
i+=1
item['V111103'] = row[i]
i+=1
item['V111104'] = row[i]
i+=1
item['V111105'] = row[i]
i+=1
item['V111106'] = row[i]
i+=1
item['V111107'] = row[i]
i+=1
item['V111108'] = row[i]
i+=1
item['T111101'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T111102'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T111103'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T111104'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T111105'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T111106'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T111107'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T111108'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['V116101'] = row[i]
i+=1
item['V116102'] = row[i]
i+=1
item['V112101'] = row[i]
i+=1
item['V112102'] = row[i]
i+=1
item['V112103'] = row[i]
i+=1
item['V112104'] = row[i]
i+=1
item['T112101'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T112102'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T112103'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['T112104'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['V109101'] = row[i]
i+=1
item['T109101'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['V110101'] = row[i]
i+=1
item['V110102'] = row[i]
i+=1
item['V101101'] = row[i]
i+=1
item['V101102'] = row[i]
i+=1
item['V102101'] = row[i]
i+=1
item['V102102'] = row[i]
i+=1
item['V108101'] = row[i]
i+=1
item['T108101'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
i+=1
item['V117101'] = row[i]
i+=1
item['T117101'] = row[i].strftime("%Y-%m-%d %H:%M:%S") if row[i] else ''
 
print 'Content-Type: application/json\n\n'
print json.dumps(item)

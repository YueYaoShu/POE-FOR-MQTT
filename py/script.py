import paho.mqtt.client
import MySQLdb
import threading
import sys
import json
import time

poeid = sys.argv[1]
pointtype = sys.argv[2]

DBClient = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mysql', db = 'MQTT',)
cursor = DBClient.cursor()
try:
  if cursor.execute("SELECT * FROM State WHERE ID='%s'"% (poeid))!=1:
    cursor.close()
    DBClient.close()
    exit(0)
except:
  cursor.close()
  DBClient.close()
  exit(0)
data = cursor.fetchone()

# Set env vars
scope = {}
i=0
scope['ID'] = data[i]
i+=1
scope['MODE'] = data[i]
i+=2
scope['I113101'] = data[i]
i+=1
scope['I113102'] = data[i]
i+=1
scope['I113103'] = data[i]
i+=1
scope['I113104'] = data[i]
i+=1
scope['I113105'] = data[i]
i+=1
scope['I113106'] = data[i]
i+=1
scope['I113107'] = data[i]
i+=1
scope['I113108'] = data[i]
i+=1
scope['I115101'] = data[i]
i+=1
scope['I115102'] = data[i]
i+=1
scope['I115103'] = data[i]
i+=1
scope['I115104'] = data[i]
i+=1
scope['I115105'] = data[i]
i+=1
scope['I115106'] = data[i]
i+=1
scope['I115107'] = data[i]
i+=1
scope['I115108'] = data[i]
i+=1
scope['I111101'] = data[i]
i+=1
scope['I111102'] = data[i]
i+=1
scope['I111103'] = data[i]
i+=1
scope['I111104'] = data[i]
i+=1
scope['I111105'] = data[i]
i+=1
scope['I111106'] = data[i]
i+=1
scope['I111107'] = data[i]
i+=1
scope['I111108'] = data[i]
i+=1
scope['T111101'] = data[i]
i+=1
scope['T111102'] = data[i]
i+=1
scope['T111103'] = data[i]
i+=1
scope['T111104'] = data[i]
i+=1
scope['T111105'] = data[i]
i+=1
scope['T111106'] = data[i]
i+=1
scope['T111107'] = data[i]
i+=1
scope['T111108'] = data[i]
i+=1
scope['I116101'] = data[i]
i+=1
scope['I116102'] = data[i]
i+=1
scope['I112101'] = data[i]
i+=1
scope['I112102'] = data[i]
i+=1
scope['I112103'] = data[i]
i+=1
scope['I112104'] = data[i]
i+=1
scope['T112101'] = data[i]
i+=1
scope['T112102'] = data[i]
i+=1
scope['T112103'] = data[i]
i+=1
scope['T112104'] = data[i]
i+=1
scope['I109101'] = data[i]
i+=1
scope['T109101'] = data[i]
i+=1
scope['I110101'] = data[i]
i+=1
scope['I110102'] = data[i]
i+=1
scope['I101101'] = data[i]
i+=1
scope['I101102'] = data[i]
i+=1
scope['I102101'] = data[i]
i+=1
scope['I102102'] = data[i]
i+=1
scope['I108101'] = data[i]
i+=1
scope['T108101'] = data[i]
i+=1
scope['I117101'] = data[i]
i+=1
scope['T117101'] = data[i]

try:
  if cursor.execute("SELECT Text FROM Script WHERE ID='%s' AND Mode=%d"% (scope['ID'], scope['MODE']))!=1:
    cursor.close()
    DBClient.close()
    exit(0)
except:
  cursor.close()
  DBClient.close()
  exit(0)  
data = cursor.fetchone()
cursor.close()
DBClient.close()

#print "----------------"+time.strftime('%Y-%m-%d %X', time.localtime(time.time()))+"----------------"
#print data[0]
#print ""
# Run it
exec(data[0], scope)

jsondata = {'device_key':scope['ID'], 'opt':'set_sensor_switch_value', 'msg':[]}
if scope.has_key('O113101') and scope['I113101']!=scope['O113101']:
  msg = {} 
  msg['st'] = '113'
  msg['sn'] = '101'
  msg['sv'] = scope['O113101']
  jsondata['msg'].append(msg)  
if scope.has_key('O113102') and scope['I113102']!=scope['O113102']:
  msg = {} 
  msg['st'] = '113'
  msg['sn'] = '102'
  msg['sv'] = scope['O113102']
  jsondata['msg'].append(msg)  
if scope.has_key('O113103') and scope['I113103']!=scope['O113103']:
  msg = {} 
  msg['st'] = '113'
  msg['sn'] = '103'
  msg['sv'] = scope['O113103']
  jsondata['msg'].append(msg)  
if scope.has_key('O113104') and scope['I113104']!=scope['O113104']:
  msg = {} 
  msg['st'] = '113'
  msg['sn'] = '104'
  msg['sv'] = scope['O113104']
  jsondata['msg'].append(msg)  
if scope.has_key('O113105') and scope['I113105']!=scope['O113105']:
  msg = {} 
  msg['st'] = '113'
  msg['sn'] = '105'
  msg['sv'] = scope['O113105']
  jsondata['msg'].append(msg)  
if scope.has_key('O113106') and scope['I113106']!=scope['O113106']:
  msg = {} 
  msg['st'] = '113'
  msg['sn'] = '106'
  msg['sv'] = scope['O113106']
  jsondata['msg'].append(msg)  
if scope.has_key('O113107') and scope['I113107']!=scope['O113107']:
  msg = {} 
  msg['st'] = '113'
  msg['sn'] = '107'
  msg['sv'] = scope['O113107']
  jsondata['msg'].append(msg)  
if scope.has_key('O113108') and scope['I113108']!=scope['O113108']:
  msg = {} 
  msg['st'] = '113'
  msg['sn'] = '108'
  msg['sv'] = scope['O113108']
  jsondata['msg'].append(msg)

MQClient = paho.mqtt.client.Client()
def sentTimepoint():  
  MQClient.publish("/timepoint", json.dumps({"device_key":poeid})) 
  MQClient.loop_stop() 
  MQClient.disconnect()
  
if len(jsondata['msg'])>0:
  MQClient.connect('127.0.0.1', 1883)#47.88.195.145 61613
  MQClient.loop_start()
  MQClient.publish('/control/%s'%(scope['ID']), json.dumps(jsondata))
  if scope['MODE']==3 and pointtype=='timepoint':
    threading.Timer(1, sentTimepoint).start()
  elif scope['MODE']==4 and pointtype=='timepoint':
    threading.Timer(10, sentTimepoint).start()
  else:
    MQClient.loop_stop()
    MQClient.disconnect()  
  exit(0)

if scope['MODE']==3 and pointtype=='timepoint':
  MQClient.connect('127.0.0.1', 1883)#47.88.195.145 61613
  MQClient.loop_start()
  threading.Timer(1, sentTimepoint).start()
elif scope['MODE']==4 and pointtype=='timepoint':
  MQClient.connect('127.0.0.1', 1883)#47.88.195.145 61613
  MQClient.loop_start()
  threading.Timer(10, sentTimepoint).start()

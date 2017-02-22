import paho.mqtt.client
import MySQLdb
import os
import multiprocessing
import json
import datetime


def script(*args):  
    enter = '%s %s %s'%('python', 'script.py', ' '.join(args))
    os.system(enter)
  
def update_state(jsonmsg):
    cursor = DBClient.cursor()
    timestring = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fields = ''
    for data in jsonmsg['datapoint']:
      fields += 'V%s%s=%f, '%(data['st'], data['sn'], data['sv']) 
      if data['st']==111 or data['st']==112 or data['st']==109 or data['st']==108 or data['st']==107:
        fields += "T%s%s='%s', "%(data['st'], data['sn'], timestring) 
    fields = fields[:-2]    
    sql = "INSERT INTO State SET ID='%s', %s ON DUPLICATE KEY UPDATE %s"%(jsonmsg['device_key'], fields, fields)
    cursor.execute(sql)
    cursor.close()
    DBClient.commit()

def save_message(id, msg):   
    cursor = DBClient.cursor()
    cursor.execute("INSERT INTO Message (ID, Content) VALUES ('%s', '%s')"% (id, msg))
    cursor.close()
    DBClient.commit()  

def do_datapoint(msg):
    jsonmsg = json.loads(msg)
    save_message(jsonmsg['device_key'], msg)
    update_state(jsonmsg)
    return (jsonmsg['device_key'], "datapoint",)

def do_timepoint(msg):
    jsonmsg = json.loads(msg)
    return (jsonmsg['device_key'], "timepoint",)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("/datapoint")
    client.subscribe("/timepoint")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):    
    if msg.topic=="/datapoint":
      multiprocessing.Process(target=script, args=do_datapoint(str(msg.payload))).start()
    if msg.topic=="/timepoint":
      multiprocessing.Process(target=script, args=do_timepoint(str(msg.payload))).start()

DBClient = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mysql', db = 'MQTT',)
MQClient = paho.mqtt.client.Client()
MQClient.on_connect = on_connect
MQClient.on_message = on_message

try:
  MQClient.connect('127.0.0.1', 1883)#47.88.195.145 61613
  MQClient.loop_forever()
except KeyboardInterrupt:  
  MQClient.disconnect()
  DBClient.close()

import MySQLdb
import paho.mqtt.client as mqtt

DBConnect = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mysql', db = 'MQTT',)
MQConnect = mqtt.Client()
MQConnect.connect('127.0.0.1', 1883)#47.88.195.145 61613

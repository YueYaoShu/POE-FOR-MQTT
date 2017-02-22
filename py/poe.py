import paho.mqtt.client as mqtt
import json

def do_message(msg):
  jsonmsg = json.loads(msg)
  jsonmsg['datapoint'] = jsonmsg.pop('msg')
  jsonmsg.pop('opt') 
  client.publish("/datapoint", json.dumps(jsonmsg))  
  
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/control/1061000001ABCDEF")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic=="/control/1061000001ABCDEF":
      do_message(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
  client.connect('127.0.0.1', 1883)
  client.loop_forever()  
except KeyboardInterrupt:  
  client.disconnect()

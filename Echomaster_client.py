import paho.mqtt.client as mqtt
import ctypes#can use dll
import time

user = ctypes.windll.user32#for use virtual key

broker = "echontrol"
#broker = "test.mosquitto.org"
#broker = "192.168.43.152"


"""

"""


received_message = ""

def on_connect(subscriber, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    print(subscriber, "connected")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subbed to", client, userdata, mid, granted_qos)

def on_message_main(subscriber,userdata, msg):
    received_message = str(msg.payload)
    print("On_message:", received_message)
    chng_tp = int(received_message[2])
    chng_amnt = int(received_message[4:-1])
    print("Parsed msg:", str(chng_tp), str(chng_amnt))
    if chng_tp == 1: #increase
        for i in range(chng_amnt):
            user.keybd_event(0xae,0,1,0) #key pressed
            user.keybd_event(0xae,0,2,0) #key unpressed
    elif chng_tp == 2: #decrease
        for i in range(chng_amnt):
            user.keybd_event(0xaf,0,1,0)
            user.keybd_event(0xAF,0,2,0)

def on_disconnect(client, userdata, rc):
    print("Disconnected", client)

def on_publish(client, userdata, mid):
    print("Published with", mid)


client = mqtt.Client()
client.on_publish = on_publish
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(broker, 1883, 60)
client.publish("echontrol_main", "connected")
client.on_message = on_message_main
client.on_publish = on_publish
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect
client.subscribe("echontrol_main", qos=1)
client.loop_forever()

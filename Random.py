
# coding: utf-8

# In[ ]:


import paho.mqtt.client as mqtt

import os,sys, time, random

tempos= []
esp_names = []

t_start = time.time()
time.sleep(1)
t_stop = time.time()
_colors = ['Azul','Amarelo','Vermelho','Roxo','Rosa','Laranja', 'Branca','Verde']
stop =False
random.seed()
def Getnames():
    client.publish(topic2, 'aaaa',0)
    while len(esp_names)<2:
        time.sleep(3)

def RandomColor(n,timeout):
    global stop,esp_names
    Getnames()
    for i in range(0,n):
        stop = False
        rdelay = random.randint(0,4)
        cor = random.choice(_colors)
        device = random.choice(esp_names)
        if timeout<10 :
            newtimeout = '0'+str(timeout)
        else:
            newtimeout = str(timeout)
        msg_buffer= device+'-'+newtimeout+'-'+cor
        print(msg_buffer)
        client.publish(topic1,msg_buffer,0)
        while(stop==False):
            time.sleep(0.010)
        time.sleep(0.200)
        time.sleep(rdelay)



def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        print("Connected Ok")
    else:
        print("rc: " + str(rc))

def on_disconnect(client, userdata, flags, rc):
        client.connected_flag=False
        print("Disconnected"+" "+str(rc))

#Callback Function
def on_message(client, obj, msg):
    global t_start ,t_stop, stop , tempos
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    msg_decode=str(msg.payload.decode("utf-8"))
    print(msg_decode)
    if msg.topic == topic1:
        msg_decode=str(msg.payload.decode("utf-8"))
        if msg_decode == 'start':
            t_start = time.time()
        if msg_decode == 'stop':
            t_stop = time.time()
            tempo = t_stop-t_start
            tempos.append(round(tempo,4))
            stop = True

    if msg.topic == topic2:
        msg_decode = str(msg.payload.decode("utf-8"))
        if msg_decode[0] == 'E':
            esp_names.append(msg_decode)
    if msg.topic == topic3:
        msg_decode = str(msg.payload.decode("utf-8"))
        Chnometer(msg_decode)




#def on_publish(client, obj, mid):

    #print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    
    cliet.not_susbscribed_flag=True
    #print("Subscribed: " + str(mid) + " " + str(granted_qos))

#def on_log(client, obj, level, string):

    print(string)

#mqtt settings
broker="192.168.4.1"
topic1 = 'test'
topic2 = 'names'
topic3 = 'time'
port = 1883
keepalive=120 #time in seconds for keepalive message
username="Aplication"
password="222"

client = mqtt.Client("python1")

# Assign event callbacks

client.on_message = on_message

client.on_connect = on_connect

client.on_disconnect=on_disconnect
#mqttc.on_publish = on_publish

mqtt.on_subscribe = on_subscribe


print("Connecting to broker",broker);

# Uncomment to enable debug messages
#client.on_log = on_log

# Connect
mqtt.Client.connected_flag=False
mqtt.Client.bad_connection_flag=False

client.username_pw_set(username , password)

# Start subscribe, with QoS level 0

client.loop_start()
client.connect(broker, port, keepalive)

while not client.connected_flag and not client.bad_connection_flag:
    print("In wait loop")
    time.sleep(1)
    if client.bad_connection_flag:
        client.loop_stop()
        sys.exit(1)

client.subscribe(topic1, 0)
client.subscribe(topic2, 0)
client.subscribe(topic3, 0)
runflag=True
#Getnames()
while runflag:
    RandomColor(30,5)
    time.sleep(2)
    for e in tempos:
        print("%.4f Segundos" % e)
    runflag=False


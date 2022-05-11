#!/usr/bin/env python3
"""a simple sensor data generator that sends to an MQTT broker via paho"""
# TODO: 
# reading puback reply, all single threaded to maintain order
# add support for amqp protocol
# implement on_publish to receive the ack
# publish over 2 different topics, alternating
import itertools
import json
import random
import timeit
import sys
import os
import json

import time
import logging

from datetime import datetime
from threading import Thread
import paho.mqtt.client as mqtt

def on_log(client, userdata, level, buf):
    print("log: ",buf)

# this is the Producer
# generating messages and reading them at the same time
def generate(host, port, topic, sensors, message, interval,iThread,aqos,username,password):
    """generate data and send it to an MQTT broker"""
    # producer client
    mqttc = mqtt.Client(client_id="python-producer")
    # adding user authn
    mqttc.username_pw_set(username, password)
    # enable logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
   
    mqttc.enable_logger(logger)
    #mqttc.on_log = on_log

    # connecting producer
    mqttc.connect(host, port)

    keys = list(sensors.keys())
    #print(keys)
    interval_secs = interval/ 1000.0
    loop = 0
    #Start timer
    start = timeit.default_timer()
    #iterate till the end last message
    while loop<(message):
        sensor_id = random.choice(keys)
        
        sensor = sensors[sensor_id]
        loop = loop + 1

        # appending current timestamp and a counter to the dict at the beginning of the msg
        updict = {"timestamp": datetime.now().isoformat()}
        updict.update(sensor)
        counter = {"counter": loop}
        # add counter to verify ordering
        counter.update(updict)
        payload = json.dumps(counter)

        #Uncomment this to check the sensor signals sent to broker
        # print("PRODUCING: %s: %s" % (topic, payload))
        mqttc.max_inflight_messages_set(60000)
        mqttc.publish(topic, payload, aqos)
        time.sleep(interval_secs)

    stop = timeit.default_timer()
    # clear cache
    sensors = {}

    #Publish the execution time for pushing the data
    print("Thread" + str(iThread + 1) + "=" + str(round((message / (stop - start)), 2)) + "msg/sec", flush=True)

    

def main(message,interval,iThread,aqos,asize,username,password):
    """main entry point, load and validate config and call generate"""
    config_path = "/cfg/config.json"
    try:
        with open(config_path) as handle:
            config = json.load(handle)
            mqtt_config = config.get("mqtt", {})
            sensors = config.get("sensors")
            # multiply the length of each sensor array by the size
            for key in iter(sensors):
                for j in range(asize):
                    acopy = sensors[key].copy()
                    for k in iter(acopy):
                        sensors[key][k+str(j)] = acopy[k]
                        
                #if key == "Sensor 1":
                #    print("Duplicated: "+str(sensors[key]),flush=True)
                
            if not sensors:
                print("no sensors specified in config.json")
                return

            host = mqtt_config.get("host", "localhost")
            port = mqtt_config.get("port", 1883)
            topic = mqtt_config.get("topic", "mqttgen")

            generate(host, port, topic, sensors,message, interval, iThread,aqos,username,password)
    except IOError as error:
        print("Error opening config file '%s'" % config_path, error)

if __name__ == '__main__':
    if len(sys.argv) == 8:
       #for multithreading
        for iThread in range(int(sys.argv[3])):
            # message interval threads QoS size username password
            Thread(target=main, args=(int(sys.argv[1]),int(sys.argv[2]),iThread, int(sys.argv[4]),int(sys.argv[5]),str(sys.argv[6]),str(sys.argv[7]))).start();
        
    else:
       print("Pass all the required parameters => mqttgen.py messageCounts messageInterval NoOfThread")
    # sleeping forever after generating all messages
    while True:
        time.sleep(60)
    
 
    # for iThread in range(5):
    #     Thread(target=main, args=(1, 0, iThread)).start();
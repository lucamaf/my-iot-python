#!/usr/bin/env python3
"""a simple sensor data generator that sends to an MQTT broker via paho"""
# TODO: generate variable payload up to 100kb based on cmd line args
# reading puback reply, all single threaded to maintain order
# add support for amqp protocol, payload size
# implement on_publish to receive the ack
# publish over 2 different topics, alternating
# add nseq number of message
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
def generate(host, port, topic, sensors, message, interval,iThread,aqos,asize):
    """generate data and send it to an MQTT broker"""
    # producer client
    mqttc = mqtt.Client(client_id="python-producer")
    # adding user authn
    mqttc.username_pw_set("sam", "iamsam")
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

        acopy = sensor.copy()
        # get a multiple of the sensor payload size based on user input
        #s=0
        #while s < asize:
        #    acopy.update(acopy)
        #    s = s + 1
            #print("counter "+str(s));

        # appending current timestamp and a counter to the dict at the beginning of the msg
        updict = {"timestamp": datetime.now().isoformat()}
        updict.update(sensor)
        counter = {"counter": loop}
        counter.update(updict)
        payload = json.dumps(counter)

        #Uncomment this to check the sensor signals sent to broker
        # print("PRODUCING: %s: %s" % (topic, payload))
        mqttc.max_inflight_messages_set(65000)
        mqttc.publish(topic, payload, aqos)
        time.sleep(interval_secs)

    stop = timeit.default_timer()
    #Publish the execution time for pushing the data
    print("Thread" + str(iThread + 1) + "=" + str(round((message / (stop - start)), 2)) + "msg/sec", flush=True)

def main(message,interval,iThread,aqos,asize):
    """main entry point, load and validate config and call generate"""
    config_path = "/cfg/config.json"
    try:
        with open(config_path) as handle:
            config = json.load(handle)
            mqtt_config = config.get("mqtt", {})
            sensors = config.get("sensors")

            if not sensors:
                print("no sensors specified in config.json")
                return

            host = mqtt_config.get("host", "localhost")
            port = mqtt_config.get("port", 1883)
            topic = mqtt_config.get("topic", "mqttgen")

            generate(host, port, topic, sensors,message, interval, iThread,aqos,asize)
    except IOError as error:
        print("Error opening config file '%s'" % config_path, error)

if __name__ == '__main__':
    if len(sys.argv) == 6:
       #for multithreading
        for iThread in range(int(sys.argv[3])):
            Thread(target=main, args=(int(sys.argv[1]),int(sys.argv[2]),iThread, int(sys.argv[4]),int(sys.argv[5]))).start();
        #sys.stdout.flush()
        
    else:
       print("Pass all the required parameters => mqttgen.py messageCounts messageInterval NoOfThread")
    # sleeping forever after generating all messages
    while True:
        time.sleep(60)
    
 
    # for iThread in range(5):
    #     Thread(target=main, args=(1, 0, iThread)).start();
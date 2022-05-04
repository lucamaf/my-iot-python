#!/usr/bin/env python3
"""a simple sensor data generator that sends to an MQTT broker via paho"""
import json
import random
import timeit
import sys
import os
import json

import time
import logging

import threading
from threading import Thread
import paho.mqtt.client as mqtt

def on_log(client, userdata, level, buf):
    print("log: ",buf)

# This is the Subscriber reading messages
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    

# this is the Producer
# generating messages and reading them at the same time
def generate(host, port, topic, sensors, message, interval,iThread):
    """generate data and send it to an MQTT broker"""
    # producer client
    mqttc = mqtt.Client(client_id="python-producer")
    # adding user authn
    mqttc.username_pw_set("sam", "iROgtC9D")
    # enable logging
    logging.basicConfig(level=logging.WARN)
    logger = logging.getLogger()
    # consumer client
    mqttcc = mqtt.Client(client_id="python-consumer")
    mqttcc.username_pw_set("rob", "lVecEu5K")

    mqttc.enable_logger(logger)
    mqttcc.enable_logger(logger)
    # mqttc.on_log = on_log

    # connecting producer and consumer
    mqttc.connect(host, port)
    mqttcc.connect(host,port)

    keys = list(sensors.keys())
    #print(keys)
    interval_secs = interval/ 1000.0
    loop = 0
    #Start timer
    start = timeit.default_timer()
    #iterate till the end last message
    while loop<(message):
        sensor_id = random.choice(keys)
        print(sensor_id)
        sensor = sensors[sensor_id]
        loop = loop + 1
        payload = json.dumps(sensor)

        #Uncomment this to check the sensor signals sent to broker
        print("PRODUCING: %s: %s" % (topic, payload))

        mqttc.publish(topic, payload)
        time.sleep(interval_secs)

        # consuming messages at the same time
        # to measure e2e throughput
        # mqttcc.consume(topic)
    stop = timeit.default_timer()
    #Publish the execution time for pushing the data
    print("Thread" + str(iThread + 1) + "=" + str(round((message / (stop - start)), 2)) + "msg/sec")

def main(message,interval,iThread):
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

            generate(host, port, topic, sensors,message, interval, iThread)
    except IOError as error:
        print("Error opening config file '%s'" % config_path, error)

if __name__ == '__main__':
    if len(sys.argv) == 4:
       #for multithreading
        for iThread in range(int(sys.argv[3])):
            Thread(target=main, args=(int(sys.argv[1]),int(sys.argv[2]),iThread)).start();
    else:
       print("Pass all the required parameters => mqttgen.py messageCounts messageInterval NoOfThread")

    # sleeping forever after generating all messages
    while True:
        time.sleep(60)
 
    # for iThread in range(5):
    #     Thread(target=main, args=(1, 0, iThread)).start();
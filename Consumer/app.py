#!/usr/bin/env python3
"""a simple MQTT consumer that reads from an MQTT broker via paho"""
import json
import random
import timeit
import sys
import os
import json

import time
import logging

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
    

# this is the Consumer
# reading messages indefinetely
def consume(host, port, topic):

    # enable logging
    logging.basicConfig(level=logging.WARN)
    logger = logging.getLogger()
    # consumer client
    mqttcc = mqtt.Client(client_id="python-consumer")
    mqttcc.username_pw_set("rob", "lVecEu5K")

    mqttcc.enable_logger(logger)
    # mqttc.on_log = on_log
    mqttcc.on_message = on_message

    # connecting producer and consumer
    mqttcc.connect(host,port)
    
    #Start timer
    # start = timeit.default_timer()
    mqttcc.subscribe(topic)
    mqttcc.loop_forever()

def main():
    """main entry point, load and validate config and call generate"""
    config_path = "/cfg/config.json"
    try:
        with open(config_path) as handle:
            config = json.load(handle)
            mqtt_config = config.get("mqtt", {})

            host = mqtt_config.get("host", "localhost")
            port = mqtt_config.get("port", 1883)
            topic = mqtt_config.get("topic", "mqttgen")

            consume(host, port, topic)
    except IOError as error:
        print("Error opening config file '%s'" % config_path, error)

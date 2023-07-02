#!/usr/bin/env python3
"""a simple MQTT consumer that reads from an MQTT broker via paho"""
import json
import timeit
import os
import json

import time
import logging

import paho.mqtt.client as mqtt

def on_log(client, userdata, level, buf):
    print("log: ",buf)

# This is the Subscriber reading messages
def on_message(client, userdata, message):
    #print("message received: " ,str(message.payload.decode("utf-8")),flush=True)
    #print("message topic = ",message.topic,flush=True)
    #print("message qos=",message.qos,flush=True)
    #print("message retain flag=",message.retain,flush=True)

    print("message received: " ,str(message.payload.decode("utf-8")))
    print("message topic = ",message.topic)
#    client.publish(message.topic, payload="", qos=2, retain=False)
 
def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
# this is the Consumer
# reading messages indefinetely
def consume(host, port, topic):

    # enable logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    # consumer client
    mqttcc = mqtt.Client(client_id="")
    mqttcc.username_pw_set("rob", "robbingbanks")

    mqttcc.enable_logger(logger)
    #mqttcc.on_log = on_log
    mqttcc.on_message = on_message
    mqttcc.on_connect = on_connect
    # connecting consumer with keepalive modified to control disconnect from broker
    mqttcc.connect(host,port,keepalive=600)
    
    #Start timer
    # start = timeit.default_timer()
    mqttcc.subscribe(topic, 2)
    mqttcc.loop_forever()
    

if __name__ == '__main__':
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

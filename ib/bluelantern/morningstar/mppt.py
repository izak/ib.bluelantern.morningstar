from time import time, sleep
from random import randint
from threading import Thread
import paho.mqtt.client as mqtt

def main(host, port, instance, name):
    client = mqtt.Client()
    client.loop_start()

    client.connect(host, port, 60)
    try:
        while True:
            now = int(time())
            pv_power = 600 + randint(-30, 35)
            bat_temp = 25 + randint(-1, 1)
            bat_volt = (245 + randint(-1, 1))/10.0

            client.publish('{}/{}/power'.format(instance, name), "{} {}".format(now, pv_power), 0)
            client.publish('{}/{}/voltage'.format(instance, name), "{} {}".format(now, bat_volt), 0)
            client.publish('{}/{}/ampere'.format(instance, name), "{} {}".format(now, pv_power/bat_volt), 0)
            client.publish('{}/{}/temperature'.format(instance, name), "{} {}".format(now, bat_temp), 0)

            sleep(1)
    except KeyboardInterrupt:
        pass
    client.disconnect()
    client.loop_stop()

def includeme(config):
    mqtt_host = config.registry.settings.get('mqtt.host')
    mqtt_port = int(config.registry.settings.get('mqtt.port', 1883))
    instance = config.registry.settings.get('morningstar.instance', 'battery01')
    name = config.registry.settings.get('morningstar.name', 'mppt')

    target = lambda: main(mqtt_host, mqtt_port, instance, name)
    thread = Thread(target = target)
    thread.daemon = True
    thread.start()

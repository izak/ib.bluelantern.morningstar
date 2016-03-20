import sys
import logging
from time import time, sleep
from threading import Thread
import paho.mqtt.client as mqtt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

logger = logging.getLogger(__name__)

def main(host, port, mqtt_username, mqtt_password, instance, name):
    modbus = ModbusClient(method='rtu', port=port, baudrate=9600, timeout=1)

    if not modbus.connect():
        logger.error("Cannot connect to modbus")
        return

    client = mqtt.Client()
    client.loop_start()

    client.connect(host, port, 60)
    if mqtt_username is not None:
        client.username_pw_set(mqtt_username, mqtt_password)

    try:
        while True:
            now = int(time())
            r = modbus.read_holding_registers(0, 16, unit=1)

            bat_volt = r.registers[8] * 96.667 * 2**(-15)
            bat_curr = r.registers[12] * 316.67 * 2**(-15)
            bat_temp = r.registers[15]

            client.publish('{}/{}/power'.format(instance, name), "{} {:0.2f}".format(now, bat_volt * bat_curr), 0)
            client.publish('{}/{}/voltage'.format(instance, name), "{} {:0.2f}".format(now, bat_volt), 0)
            client.publish('{}/{}/current'.format(instance, name), "{} {:0.2f}".format(now, bat_curr), 0)
            client.publish('{}/{}/temperature'.format(instance, name), "{} {}".format(now, bat_temp), 0)

            sleep(5)
    except KeyboardInterrupt:
        pass
    client.disconnect()
    client.loop_stop()
    modbus.close()

def includeme(config):
    mqtt_host = config.registry.settings.get('mqtt.host')
    mqtt_port = int(config.registry.settings.get('mqtt.port', 1883))
    instance = config.registry.settings.get('morningstar.instance', 'battery01')
    name = config.registry.settings.get('morningstar.name', 'mppt')

    serial_port = config.registry.settings.get('morningstar.port')

    target = lambda: main(mqtt_host, mqtt_port, instance, name)
    thread = Thread(target = target)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    main('localhost', 1883, None, None, 'battery01', 'mppt', sys.argv[1])

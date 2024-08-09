from machine import Pin
from dht import DHT22

dht22_sensor = None
led = None

def initialize_sensors():
    global dht22_sensor, led
    
    dht22_sensor = DHT22(Pin(0, Pin.IN, Pin.PULL_UP))
    led = Pin("LED", Pin.OUT)
    
def get_led():
    global led
    return led

def get_dht22_sensor():
    global dht22_sensor
    return dht22_sensor


def measure():
    global dht22_sensor
    
    dht22_sensor.measure()
    temp = dht22_sensor.temperature()
    humi = dht22_sensor.humidity()

    return temp, humi
from machine import Pin, ADC
from dht import DHT22

dht22_sensor = None
photo_resistor = None
raindrop_sensor = None
led = None

def initialize_sensors():
    global dht22_sensor, photo_resistor, raindrop_sensor, led
    
    dht22_sensor = DHT22(Pin(0, Pin.IN, Pin.PULL_UP))
    raindrop_sensor = Pin(16, Pin.IN)
    photo_resistor = ADC(0)
    led = Pin("LED", Pin.OUT)
    
def get_led():
    global led
    return led
    
def convert_light_value_to_percent(value):
    return round((value / 65536) * 100, 1)
    
def measure():
    global dht22_sensor, photo_resistor, raindrop_sensor
    
    dht22_sensor.measure()
    temp_value = dht22_sensor.temperature()
    humi_value = dht22_sensor.humidity()
    light = 65536 - photo_resistor.read_u16()
    rain_value = 1 if raindrop_sensor.value() == 0 else 0
    
    light_value = convert_light_value_to_percent(light)
    
    return round(temp_value, 1), round(humi_value, 1), light_value, rain_value

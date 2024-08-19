from machine import Pin, ADC
from dht import DHT22

dht22_sensor = None
photo_resistor = None
raindrop_sensor = None
led = None
    
def initialize_led():
    global led
    led = Pin("LED", Pin.OUT)
    
def initialize_dht22():
    global dht22_sensor
    dht22_sensor = DHT22(Pin(0, Pin.IN, Pin.OUT))
    
def initialize_photo_resistor():
    global photo_resistor
    photo_resistor = ADC(0)
    
def initialize_raindrop_sensor():
    global raindrop_sensor
    raindrop_sensor = raindrop_sensor = Pin(16, Pin.IN)
    
def get_led():
    global led
    return led

def __convert_light_value_to_percent(value):
    return round((value / 65536) * 100, 1)

def measure_dht22():
    global dht22_sensor
    
    dht22_sensor.measure()
    temp = dht22_sensor.temperature()
    humi = dht22_sensor.humidity()

    return round(temp, 1), round(humi, 1)

def measure_photo_resistor():
    global photo_resistor
    
    light = 65536 - photo_resistor.read_u16()
    
    return __convert_light_value_to_percent(light)
    
def measure_raindrop():
    global raindrop_sensor
    
    return 1 if raindrop_sensor.value() == 0 else 0

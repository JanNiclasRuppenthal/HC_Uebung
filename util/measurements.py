from machine import Pin, ADC
from dht import DHT22

from wifi.http_request import get_outdoor_sensor_value

UPDATE_RATE = 10

class Measure():
    def __init__(self):
        # Sensors
        self.dht22_sensor = None
        self.photo_resistor = None
        self.raindrop_sensor = None
        self.led = None
    
    def initialize_led(self):
        self.led = Pin("LED", Pin.OUT)
        
    def initialize_dht22(self):
        self.dht22_sensor = DHT22(Pin(0, Pin.IN, Pin.OUT))
        
    def initialize_photo_resistor(self):
        self.photo_resistor = ADC(0)
        
    def initialize_raindrop_sensor(self):
        self.raindrop_sensor = raindrop_sensor = Pin(16, Pin.IN)

    def __convert_light_value_to_percent(self, value):
        return round((value / 65536) * 100, 1)

    def __measure_dht22(self):
        self.dht22_sensor.measure()
        temp = self.dht22_sensor.temperature()
        humi = self.dht22_sensor.humidity()

        return round(temp, 1), round(humi, 1)

    def __measure_photo_resistor(self):
        light = 65536 - self.photo_resistor.read_u16()
        
        return self.__convert_light_value_to_percent(light)
        
    def __measure_raindrop(self):
        return 1 if self.raindrop_sensor.value() == 0 else 0


class Indoor_Measure(Measure):
    def __init__(self):
        super().__init__()
        
        # Indoor values
        self.temp_value = -1
        self.humi_value = -1
        self.temp_queue = [0] * ((60 // UPDATE_RATE) * 24)
        self.humi_queue = [0] * ((60 // UPDATE_RATE) * 24)

        # Outdoor values for the ePaper display
        self.temp_outdoor_value = -1
        self.humi_outdoor_value = -1
        self.rain_outdoor_value = -1
        self.light_outdoor_value = -1
        
        
        # Last read values
        self.last_temp = -1
        self.last_humi = -1
        self.last_temp_outdoor = -1
        self.last_humi_outdoor = -1
        self.last_rain_outdoor = -1
        self.last_light_outdoor = -1
    
    def set_indoor_values(self):
        self.temp_value, self.humi_value = self.__measure_dht22()
                
        self.temp_queue.pop(0)
        self.temp_queue.append(self.temp_value)
        self.humi_queue.pop(0)
        self.humi_queue.append(self.humi_value)
        
    def set_outdoor_values_http(self):
        self.temp_outdoor_value = get_outdoor_sensor_value('/temp_value')
        self.humi_outdoor_value = get_outdoor_sensor_value('/humi_value')
        self.rain_outdoor_value = get_outdoor_sensor_value('/rain_value')
        self.light_outdoor_value = get_outdoor_sensor_value('/light_value')
    


class Outdoor_Measure(Measure):
    def __init__(self):
        super().__init__()
        
        self.temp_value = -1
        self.humi_value = -1
        self.rain_value = -1
        self.light_value = -1
        
    def set_outdoor_values(self):
        self.temp_value, self.humi_value = self.__measure_dht22()
        self.light_value = self.__measure_photo_resistor()
        self.rain_value = self.__measure_raindrop()

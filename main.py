from machine import Pin
from time import sleep
from dht import DHT22

# initialize DHT22 sensor
dht22_sensor = DHT22(Pin(0, Pin.IN, Pin.PULL_UP))

while True:
    try:
        # begin measure
        dht22_sensor.measure()
        temp = dht22_sensor.temperature()
        humi = dht22_sensor.humidity()
        
        # print the measure stats to the terminal
        print('Temperatur:', temp, '°C')
        print('Luftfeuchtigkeit:', humi, '%')
    except Exception as e:
        print('Got an exception: ' + str(e))
    sleep(2)
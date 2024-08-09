from machine import Pin, ADC
import time


raindrop_sensor = Pin(16, Pin.IN)
photo_resistor = ADC(0)

while True:
    if raindrop_sensor.value() == 0:
        print("Raindrop detected!")
    else:
        print("Monitoring...") 
    
    light_value = photo_resistor.read_u16()
    print(f"ADC: {light_value}")

    time.sleep(1)
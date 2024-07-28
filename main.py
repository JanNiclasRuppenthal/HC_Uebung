from machine import Pin, RTC
import time
from dht import DHT22
from Pico_ePaper import EPD_2in9_Landscape

weekday_str_list = [
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag"
]



def setup_display(e_display):
    e_display.Clear(0xff)
    e_display.fill(0xff)
    #title
    e_display.text("Wetterstation", 5, 0, 0x00)
    e_display.text("Raspberry Pi Pico W", 5, 10, 0x00)
    
    # date
    date = RTC().datetime()
    weekday_number = date[3]
    weekday_str = weekday_str_list[weekday_number]
    e_display.text(weekday_str, 210, 0, 0x00)
    date_str = "{:02d}.{:02d}.{:d}".format(date[2], date[1], date[0])
    e_display.text(date_str, 210, 10, 0x00)
    
    # ip address
    ip_str = "IP Address: X.X.X.X".format()
    e_display.text(ip_str, 5, 121, 0x00)
    
    # owner
    owner_str = "JNR#33"
    e_display.text(owner_str, 210, 121, 0x00)
    
    # lines
    e_display.hline(0, 20, 296, 0x00)
    e_display.hline(0, 115, 296, 0x00)
    
    # show result on display
    e_display.display(e_display.buffer)

    
def main():
    # initialize DHT22 sensor
    dht22_sensor = DHT22(Pin(0, Pin.IN, Pin.PULL_UP))
    
    e_display = EPD_2in9_Landscape()
    setup_display(e_display)
    
    while True:
        try:
            # begin measure
            dht22_sensor.measure()
            temp = dht22_sensor.temperature()
            humi = dht22_sensor.humidity()
            
            # print the measure stats to the terminal
            print('Temperatur: {:.1f} °C'.format(temp))
            print('Luftfeuchtigkeit: {:.1f} %'.format(humi))
        except Exception as e:
            print('Got an exception: ' + str(e))
        time.sleep(2)

if __name__=='__main__':
    main()
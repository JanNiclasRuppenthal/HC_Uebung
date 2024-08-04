from machine import Pin, RTC
import time
import ntptime
from dht import DHT22
from Pico_ePaper import EPD_2in9_Landscape
from web_server import connect, open_socket, webpage
import select

weekday_str_list = [
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag"
]

temp = 0
humi = 0

def setup_display(e_display):
    e_display.Clear(0xff)
    e_display.fill(0xff)
    # title
    e_display.text("Wetterstation", 5, 0, 0x00)
    e_display.text("Raspberry Pi Pico W", 5, 10, 0x00)
    
    # date
    date = RTC().datetime()
    weekday_number = date[3]
    weekday_str = weekday_str_list[weekday_number]
    e_display.text(weekday_str, 210, 0, 0x00)
    date_str = "{:02d}.{:02d}.{:d}".format(date[2], date[1], date[0])
    e_display.text(date_str, 210, 10, 0x00)
    
    # temperature
    temp_str = "Temperatur: "
    e_display.text(temp_str, 5, 50, 0x00)
    e_display.text("     Grad", 120, 50, 0x00)
    
    # humidity
    hum_str = "Feuchtigkeit: "
    e_display.text(hum_str, 5, 75, 0x00)
    e_display.text("     %", 120, 75, 0x00)
    
    # static ip address
    ip_str = "IP Adresse: "
    e_display.text(ip_str, 5, 121, 0x00)
    
    # owner
    owner_str = "JNR#33"
    e_display.text(owner_str, 245, 121, 0x00)
    
    # lines
    e_display.hline(0, 20, 296, 0x00)
    e_display.hline(0, 115, 296, 0x00)
    
    # show result on display
    e_display.display(e_display.buffer)

def run_server(connection):
    global temp, humi
    try:
        ready_to_read, _, _ = select.select([connection], [], [], 1)
        if ready_to_read:
            client, _ = connection.accept()
            request = client.recv(1024)  # Receive the request data
            #request = str(request)
            #print("Request:", request)
            
            html = webpage(temp, humi)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html
            client.send(response)
            client.close()
    except Exception as e:
        print('Got an exception in run_server: ' + str(e))
        machine.reset()

def main():
    global temp, humi

    # initialize DHT22 sensor
    dht22_sensor = DHT22(Pin(0, Pin.IN, Pin.PULL_UP))
    led = Pin("LED", Pin.OUT)

    try:
        ip = connect()
        connection = open_socket(ip)
    except KeyboardInterrupt:
        machine.reset()
        
    ntptime.settime()
    
    e_display = EPD_2in9_Landscape()
    setup_display(e_display)
    last_temp = -1
    last_humi = -1
    change = False
        
    led.on()
    e_display.text(ip, 100, 121, 0x00)
    e_display.display_Partial(e_display.buffer)
    led.off()
    
    while True:
        try:
            # begin measure
            dht22_sensor.measure()
            temp = dht22_sensor.temperature()
            humi = dht22_sensor.humidity()
            
            if last_temp != temp:
                temp_str = "{:.1f}".format(temp)
                e_display.fill_rect(120, 50, 35, 10, 0xff)
                e_display.text(temp_str, 120, 50, 0x00)
                
                change = True
                last_temp = temp
                
            if last_humi != humi:
                humi_str = "{:.1f}".format(humi)
                e_display.fill_rect(120, 75, 35, 10, 0xff)
                e_display.text(humi_str, 120, 75, 0x00)
                
                change = True
                last_humi = humi
                
            if change:
                led.on()
                e_display.display_Partial(e_display.buffer)
                change = False
                led.off()
            
            # Handle web server
            run_server(connection)
            
        except Exception as e:
            print('Got an exception: ' + str(e))
        time.sleep(2)

if __name__=='__main__':
    main()

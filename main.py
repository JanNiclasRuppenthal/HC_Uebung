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

UPDATE_RATE = 5

temp = 0
humi = 0
temp_queue = [0] * ((60 // UPDATE_RATE) * 24)
humi_queue = [0] * ((60 // UPDATE_RATE) * 24)
hour = 0

def is_summertime(t):
    year = t[0]
    month = t[1]
    day = t[2]
    weekday = t[6]  # Monday is 0 and Sunday is 6

    # DST starts at 2:00 AM on the last Sunday in March
    # Find the last Sunday in March
    last_sunday_march = 31 - (((time.localtime(time.mktime((2024, 3, 31, 3, 0, 0, 0, 0, 0)))[6]) + 1) % 7)
    dst_start = time.mktime((year, 3, last_sunday_march, 2, 0, 0, 0, 0, 0))

    # DST ends at 3:00 AM on the last Sunday in October
    # Find the last Sunday in October
    last_sunday_october = 31 - (((time.localtime(time.mktime((2024, 3, 31, 3, 0, 0, 0, 0, 0)))[6]) + 1) % 7)
    dst_end = time.mktime((year, 10, last_sunday_october, 3, 0, 0, 0, 0, 0))

    current_time = time.mktime(t)
    return dst_start <= current_time < dst_end


def setup_display(e_display):
    e_display.Clear(0xff)
    e_display.fill(0xff)
    # title
    e_display.text("Wetterstation", 5, 0, 0x00)
    e_display.text("Raspberry Pi Pico W", 5, 10, 0x00)
    
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
    

def mark_exception_on_display(e_display):
    e_display.line(250, 70, 276, 70, 0x00)
    e_display.line(250, 70, 264, 50, 0x00)
    e_display.line(276, 70, 264, 50, 0x00)
    e_display.text("!", 260, 60, 0x00)
    e_display.display_Partial(e_display.buffer)

def run_server(connection):
    global temp, humi, temp_queue, humi_queue, hour
    try:
        ready_to_read, _, _ = select.select([connection], [], [], 1)
        if ready_to_read:
            client, _ = connection.accept()
            request = client.recv(1024)  # Receive the request data
            
            html = webpage(temp, humi, temp_queue, humi_queue, hour)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html
            client.send(response)
            client.close()
    except Exception as e:
        mark_exception_on_display(e_display)
        machine.reset()


def main():
    global temp, humi, temp_queue, humi_queue, hour

    # initialize DHT22 sensor
    dht22_sensor = DHT22(Pin(0, Pin.IN, Pin.PULL_UP))
    led = Pin("LED", Pin.OUT)

    try:
        ip = connect()
        connection = open_socket(ip)
    except KeyboardInterrupt:
        machine.reset()
        
    e_display = EPD_2in9_Landscape()
    setup_display(e_display)
    last_temp = -1
    last_humi = -1
    last_weekday_number = -1
    change = False
    count = -1
    
    
    # date
    ntptime.settime()
    
    # Differantiate between Summer and Winter time in Germany
    if is_summertime(time.localtime()):
        UTC_OFFSET = 2 * 60 * 60 
    else:
        UTC_OFFSET = 1 * 60 * 60
    
        
    led.on()
    e_display.text(ip, 100, 121, 0x00)
    e_display.display_Partial(e_display.buffer)
    led.off()
    
    while True:
        
        run_server(connection)
        
        if (count == -1 or count >= 1): #UPDATE_RATE * 60):
            count = 0
        
            try:
                date = time.localtime(time.time() + UTC_OFFSET)
                weekday_number = date[6]
                hour = date[3]
                
                if last_weekday_number != weekday_number:
                    weekday_str = weekday_str_list[weekday_number]
                    e_display.text(weekday_str, 210, 0, 0x00)
                    date_str = "{:02d}.{:02d}.{:d}".format(date[2], date[1], date[0])
                    e_display.text(date_str, 210, 10, 0x00)
                    change = True
                    
                    last_weekday_number = weekday_number
                
                # begin measure
                dht22_sensor.measure()
                temp = dht22_sensor.temperature()
                humi = dht22_sensor.humidity()
                
                temp_queue.pop(0)
                temp_queue.append(temp)
                humi_queue.pop(0)
                humi_queue.append(humi)
                
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
        
            except Exception as e:
                mark_exception_on_display(e_display)
                time.sleep(2)
                
        time.sleep(0.1)
        count += 0.1

if __name__ == '__main__':
    main()
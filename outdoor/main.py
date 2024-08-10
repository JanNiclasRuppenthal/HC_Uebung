import time
import select

from util.measurements import *
from wifi.web_server import *

UPDATE_RATE = 60

temp_value = -1
humi_value = -1
rain_value = -1
light_value = -1

def run_server(connection):
    global temp_value, humi_value, light_value, rain_value
    
    try:
        ready_to_read, _, _ = select.select([connection], [], [], 1)
        if ready_to_read:
            led = get_led()
            led.on()
            conn, addr = connection.accept()
            request = conn.recv(1024)
            request = str(request)

            if '/temp_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{temp_value}"
            elif '/humi_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{humi_value}"
            elif '/rain_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{rain_value}"
            elif '/light_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{light_value}"
            else:
                html_webpage = webpage_outdoor(temp_value, humi_value, light_value, rain_value)
                response = "HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n" + html_webpage

            conn.send(response)
            conn.close()
            led.off()
            
    except OSError as e:
        machine.reset()
        

def main():
    global temp_value, humi_value, light_value, rain_value
    
    initialize_sensors()
    led = get_led()
    
    
    led.on()
    
    try:
        connection, ip = connect_to_wifi()
    except Exception as e:
        machine.reset()
      
    led.off()

    count = -1
    while True:
        if (count == -1 or count >= UPDATE_RATE * 60):
            count = 0
            temp_value, humi_value, light_value, rain_value = measure()

        time.sleep(1)
        count += 1
        
        run_server(connection)
        
if __name__ == '__main__':
    main()

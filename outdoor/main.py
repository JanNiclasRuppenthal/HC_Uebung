import time
import select
import gc

from util.measurements import *
from util.config_date import get_first_digit_of_minute
from util.logging import log_exception
from wifi.web_server import *

measure = Outdoor_Measure()

def run_server(connection):
    try:
        ready_to_read, _, _ = select.select([connection], [], [], 1)
        if ready_to_read:
            measure.led.on()
            conn, addr = connection.accept()
            request = conn.recv(1024)
            request = str(request)

            if '/temp_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{measure.temp_value}"
            elif '/humi_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{measure.humi_value}"
            elif '/rain_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{measure.rain_value}"
            elif '/light_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{measure.light_value}"
            else:
                html_webpage = webpage_outdoor(measure.temp_value, measure.humi_value, measure.light_value, measure.rain_value)
                response = "HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n" + html_webpage

            conn.send(response)
            conn.close()
            measure.led.off()
            
            # clear memory
            gc.collect() 
            
    except Exception as e:
        log_exception(e)
        machine.reset()


def main():
    measure.initialize_led()
    measure.initialize_dht22()
    measure.initialize_photo_resistor()
    measure.initialize_raindrop_sensor()
       
    measure.led.on()
    
    try:
        connection, ip = connect_to_wifi()
    except Exception as e:
        log_exception(e)
        machine.reset()
      
    measure.led.off()

    first_digit_of_minute = -1
    count_sec = -1
    
    while True:
        if (count_sec == -1 or count_sec == 60):
            temp_first_digit_minute = get_first_digit_of_minute()
            count = 0
            
        if (first_digit_of_minute != temp_first_digit_minute):
            first_digit_of_minute = temp_first_digit_minute
        
            try:
                measure.set_outdoor_values()
                
                # clear memory
                gc.collect() 
                
            except Exception as e:
                log_exception(e)
                machine.reset()
                
        time.sleep(1)
        count_sec += 1
        
        run_server(connection)
        
if __name__ == '__main__':
    main()

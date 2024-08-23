import time
import select
import gc

from display.config_display import *
from wifi.web_server import *
from util.config_date import *
from util.measurements import *
from util.logging import log_exception
from wifi.wifi_configuration import server_ip

measure = Indoor_Measure()
display = Display()


def run_server(connection):
    client = None
    try:
        ready_to_read, _, _ = select.select([connection], [], [], 1)
        if ready_to_read:
            client, _ = connection.accept()
            request = client.recv(1024)
            
            html_webpage = webpage_indoor(measure.temp_value, measure.humi_value, measure.temp_queue, measure.humi_queue)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html_webpage
            client.send(response)
            client.close()
            
            # clear memory
            gc.collect()
    except Exception as e:
        display.mark_exception_on_display()
        log_exception(e)
        machine.reset()
        

        
def update_date_values(UTC_OFFSET, last_weekday_number):  
    date = time.localtime(time.time() + UTC_OFFSET)
    weekday_number = date[6]
    if last_weekday_number != weekday_number:
        display.update_date_on_display(weekday_number, date)
        last_weekday_number = weekday_number
        
    return last_weekday_number
    
        
def update_measure_values():    
    measure.set_indoor_values()
    measure.set_outdoor_values_http()
    
    display.set_values_to_buffer(measure)
    
    measure.led.on()
    display.update_display()
    measure.led.off()
        
def main():
    measure.initialize_led()
    measure.initialize_dht22()
    display.setup_display()

    try:
        connection, ip = connect_to_wifi()
    except Exception as e:
        display.mark_exception_on_display()
        log_exception(e)
        machine.reset()
    
    display.add_IP_to_display(ip)

    set_date_time_NTP()

    UTC_OFFSET = -1
    last_weekday_number = -1
    first_digit_of_minute = -1
    temp_first_digit_minute = -1

    while True:
        temp_first_digit_minute = get_first_digit_of_minute()
        if (first_digit_of_minute != temp_first_digit_minute):
            first_digit_of_minute = temp_first_digit_minute

            try:
                UTC_OFFSET = calculate_UTC_offset(time.localtime())
                last_weekday_number = update_date_values(UTC_OFFSET, last_weekday_number)
                update_measure_values()
                
                # clear memory
                gc.collect() 
            except Exception as e:
                display.mark_exception_on_display()
                log_exception(e)
                time.sleep(2)
                
        time.sleep(1)
        
        run_server(connection)
        

if __name__ == '__main__':
    main()
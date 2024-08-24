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


def check_and_update_values():
    change = False
    
    if (measure.last_temp != measure.temp_value):
        display.set_value_to_buffer(measure.temp_value, 120, 50)
        measure.last_temp = measure.temp_value
        change = True
        
    if (measure.last_humi != measure.humi_value):
        display.set_value_to_buffer(measure.humi_value, 120, 75)
        measure.last_humi = measure.temp_value
        change = True
    
    if (measure.last_temp_outdoor != measure.temp_outdoor_value):
        display.set_value_to_buffer(measure.temp_outdoor_value, 220, 25)
        measure.last_temp_outdoor = measure.temp_outdoor_value
        change = True
    
    if (measure.last_humi_outdoor != measure.humi_outdoor_value):
        display.set_value_to_buffer(measure.humi_outdoor_value, 220, 50)
        measure.last_humi_outdoor = measure.humi_outdoor_value
        change = True
    
    if (measure.last_light_outdoor != measure.light_outdoor_value):
        display.set_value_to_buffer(measure.light_outdoor_value, 220, 75)
        measure.last_light_outdoor = measure.light_outdoor_value
        change = True
        
    if (measure.last_rain_outdoor != measure.rain_outdoor_value):
        display.set_value_to_buffer(measure.rain_outdoor_value, 220, 100, False)
        measure.last_rain_outdoor = measure.rain_outdoor_value
        change = True
    
    return change


def update_measure_values():    
    measure.set_indoor_values()
    measure.set_outdoor_values_http()
    
    change = check_and_update_values()
        
    if (change):
        measure.led.on()
        display.update_display()
        measure.led.off()
        change = False


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
    count = -1

    while True:
        if (count == -1 or count == 60):
            temp_first_digit_minute = get_first_digit_of_minute()
            count = 0
            
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
        count += 1
        
        run_server(connection)
        

if __name__ == '__main__':
    main()
import time
import select

from display.config_display import *
from wifi.web_server import *
from util.config_date import *
from util.measurements import *
from wifi.http_request import get_outdoor_sensor_value
from wifi.wifi_configuration import server_ip

UPDATE_RATE = 10

# indoor
temp_value = 0
humi_value = 0
temp_queue = [0] * ((60 // UPDATE_RATE) * 24)
humi_queue = [0] * ((60 // UPDATE_RATE) * 24)

# outdoor
temp_outdoor_value = 0
humi_outdoor_value = 0
rain_outdoor_value = 0
light_outdoor_value = 0


def run_server(connection):
    global temp_value, humi_value
    global temp_queue, humi_queue
    
    try:
        ready_to_read, _, _ = select.select([connection], [], [], 1)
        if ready_to_read:
            client, _ = connection.accept()
            request = client.recv(1024) 
            
            html = webpage_indoor(temp_value, humi_value, temp_queue, humi_queue)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html
            client.send(response)
            client.close()
    except Exception as e:
        mark_exception_on_display()
        print(f"Exception in run_server: {e}")
        machine.reset()
        
def update_date_values(UTC_OFFSET, last_weekday_number):  
    date = time.localtime(time.time() + UTC_OFFSET)
    weekday_number = date[6]
    if last_weekday_number != weekday_number:
        update_date_on_display(weekday_number, date)
        last_weekday_number = weekday_number
        
    return last_weekday_number
        
def update_measure_values(last_temp, last_humi, last_temp_outdoor, last_humi_outdoor, last_rain_outdoor, last_light_outdoor):
    global temp_value, humi_value
    global temp_queue, humi_queue
    global temp_outdoor_value, rain_outdoor_value, light_outdoor_value
    
    # indoor
    temp_value, humi_value = measure_dht22()
                
    temp_queue.pop(0)
    temp_queue.append(temp_value)
    humi_queue.pop(0)
    humi_queue.append(humi_value)
    
    # outdoor
    temp_outdoor_value = get_outdoor_sensor_value('/temp_value')
    humi_outdoor_value = get_outdoor_sensor_value('/humi_value')
    rain_outdoor_value = get_outdoor_sensor_value('/rain_value')
    light_outdoor_value = get_outdoor_sensor_value('/light_value')
    
    change = False
    
    if last_temp != temp_value:
        set_value_to_buffer(temp_value, 120, 50)
        change = True
        last_temp = temp_value
        
    if last_humi != humi_value:
        set_value_to_buffer(humi_value, 120, 75)
        change = True
        last_humi = humi_value
        
    
    if last_temp_outdoor != temp_outdoor_value:
        set_value_to_buffer(temp_outdoor_value, 220, 25)
        change = True
        last_temp_outdoor = temp_outdoor_value
        
    if last_humi_outdoor != humi_outdoor_value:
        set_value_to_buffer(humi_outdoor_value, 220, 50)
        change = True
        last_humi_outdoor = humi_outdoor_value
        
    if last_light_outdoor != light_outdoor_value:
        set_value_to_buffer(light_outdoor_value, 220, 75)
        change = True
        last_light_outdoor = light_outdoor_value
        
    if last_rain_outdoor != rain_outdoor_value:
        set_value_to_buffer(rain_outdoor_value, 220, 100, False)
        change = True
        last_rain_outdoor = rain_outdoor_value
        
    if change:
        get_led().on()
        update_display()
        change = False
        get_led().off()
        
    return last_temp, last_humi, last_temp_outdoor, last_humi_outdoor, last_rain_outdoor, last_light_outdoor

def main():
    initialize_led()
    initialize_dht22()
    setup_display()
    
    try:
        connection, ip = connect_to_wifi()
    except Exception as e:
        mark_exception_on_display()
        print(f"Exception while connecting: {e}")
        machine.reset()
        
    add_IP_to_display(ip)
    
    # date
    set_date_time_NTP()
    UTC_OFFSET = -1
    
    last_temp = -1
    last_humi = -1
    last_weekday_number = -1
    
    last_temp_outdoor = -1
    last_humi_outdoor = -1
    last_rain_outdoor = -1
    last_light_outdoor = -1
    
    first_digit_of_minute = -1
    
    
    while True:
        temp_first_digit_minute = get_first_digit_of_minute()
        if (first_digit_of_minute != temp_first_digit_minute):
            first_digit_of_minute = temp_first_digit_minute
        
            try:
                UTC_OFFSET = calculate_UTC_offset(time.localtime())
                last_weekday_number = update_date_values(UTC_OFFSET, last_weekday_number)
                    
                last_temp, last_humi, last_temp_outdoor, last_humi_outdoor, last_rain_outdoor, last_light_outdoor = update_measure_values(last_temp, last_humi, last_temp_outdoor, last_humi_outdoor, last_rain_outdoor, last_light_outdoor)
                
            except Exception as e:
                mark_exception_on_display()
                print(f"Exception while connecting: {e}")
                time.sleep(2)
                
        time.sleep(0.1)
        
        run_server(connection)

if __name__ == '__main__':
    main()
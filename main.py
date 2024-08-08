import time
import select

from display.config_display import *
from wifi.web_server import connect_to_wifi, webpage
from util.config_date import *
from util.measurements import *

UPDATE_RATE = 10
temp_value = 0
humi_value = 0
temp_queue = [0] * ((60 // UPDATE_RATE) * 24)
humi_queue = [0] * ((60 // UPDATE_RATE) * 24)
hour = 0

def run_server(connection):
    global temp_value, humi_value, temp_queue, humi_queue
    
    try:
        ready_to_read, _, _ = select.select([connection], [], [], 1)
        if ready_to_read:
            client, _ = connection.accept()
            request = client.recv(1024)  # Receive the request data
            
            html = webpage(temp_value, humi_value, temp_queue, humi_queue)
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
        
def update_measure_values(last_temp, last_humi):
    global temp_value, humi_value, temp_queue, humi_queue
    
    temp, humi = measure()
    
    temp_value = round(temp, 1)
    humi_value = round(humi, 1)
                
    temp_queue.pop(0)
    temp_queue.append(temp_value)
    humi_queue.pop(0)
    humi_queue.append(humi)
    
    change = False
    
    if last_temp != temp_value:
        set_temperature_to_buffer(temp_value)
        
        change = True
        last_temp = temp_value
        
    if last_humi != humi_value:
        set_humidity_to_buffer(humi_value)
        change = True
        last_humi = humi_value
        
    if change:
        get_led().on()
        update_display()
        change = False
        get_led().off()
        
    return last_temp, last_humi


def main():
    initialize_sensors()
    setup_display()
    
    try:
        connection, ip = connect_to_wifi()
    except Exception as e:
        mark_exception_on_display()
        print(f"Exception while connecting: {e}")
        machine.reset()
    
    last_temp = -1
    last_humi = -1
    last_weekday_number = -1
    change = False
    count = -1
    
    # date
    set_date_time_NTP()
    UTC_OFFSET = -1
    
    add_IP(ip)
    
    
    while True:
        
        if (count == -1 or count >= UPDATE_RATE * 60):
            count = 0
        
            try:
                # Differantiate between Summer and Winter time in Germany
                UTC_OFFSET = calculate_UTC_offset(time.localtime())
                last_week_day_number = update_date_values(UTC_OFFSET, last_weekday_number)
                    
                last_temp, last_humi = update_measure_values(last_temp, last_humi)
                
            except Exception as e:
                mark_exception_on_display()
                print(f"Exception in main: {e}")
                time.sleep(2)
                
        time.sleep(1)
        count += 1
        
        run_server(connection)

if __name__ == '__main__':
    main()
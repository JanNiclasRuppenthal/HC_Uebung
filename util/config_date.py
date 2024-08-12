import ntptime
import time

weekday_str_list = [
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag"
]

def set_date_time_NTP():
    ntptime.settime()
    
def get_first_digit_of_minute():
    # There is no need to add the UTC_OFFSET
    # because we only need the minutes
    date = time.localtime(time.time())
    minute = date[4]
    
    if (10 <= minute <= 19):
        return 1
    elif (20 <= minute <= 29):
        return 2
    elif (30 <= minute <= 39):
        return 3
    elif (40 <= minute <= 49):
        return 4
    elif (50 <= minute <= 59):
        return 5
    else:
        return 0
    
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

def calculate_UTC_offset(time):
    UTC_OFFSET = -1
    
    # Differantiate between Summer and Winter time in Germany
    if is_summertime(time):
        UTC_OFFSET = 2 * 60 * 60 
    else:
        UTC_OFFSET = 1 * 60 * 60
        
    return UTC_OFFSET
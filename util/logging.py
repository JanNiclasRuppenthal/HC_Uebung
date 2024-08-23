import sys
import time
from util.config_date import calculate_UTC_offset

def log_exception(e):
    with open("log.txt", "a") as f:
        UTC_OFFSET = calculate_UTC_offset(time.localtime())
        date = time.localtime(time.time() + UTC_OFFSET)
        date_str = "{:02d}.{:02d}.{:d}".format(date[2], date[1], date[0])
        clock_str = "{:02d}:{:02d}".format(date[4], date[3])
        f.write(f"At {date_str} {clock_str} I got the following exception: {e}\n")
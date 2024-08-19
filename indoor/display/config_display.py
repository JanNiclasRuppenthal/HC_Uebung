from display.Pico_ePaper import EPD_2in9_Landscape
from util.config_date import weekday_str_list

e_display = EPD_2in9_Landscape()

def setup_display():
    global e_display
    
    e_display.Clear(0xff)
    e_display.fill(0xff)
    
    # title
    e_display.text("Wetterstation", 5, 0, 0x00)
    e_display.text("Raspberry Pi Pico W", 5, 10, 0x00)
    
    # temperature
    temp_str = "Temperatur: "
    e_display.text(temp_str, 5, 50, 0x00)
    e_display.text("     Grad", 120, 50, 0x00)
    e_display.text("     Grad", 220, 25, 0x00)
    
    # humidity
    hum_str = "Feuchtigkeit: "
    e_display.text(hum_str, 5, 75, 0x00)
    e_display.text("     %", 120, 75, 0x00)
    
    # outdoor values
    e_display.text("     %", 220, 50, 0x00)
    e_display.text("     %", 220, 75, 0x00)
    
    # static ip address
    ip_str = "IP-Adresse: "
    e_display.text(ip_str, 5, 121, 0x00)
    
    # owner
    owner_str = "JNR#33"
    e_display.text(owner_str, 245, 121, 0x00)
    
    # lines
    e_display.hline(0, 20, 296, 0x00)
    e_display.hline(0, 115, 296, 0x00)
    e_display.vline(210, 20, 95, 0x00)
    
    # show result on display
    e_display.display(e_display.buffer)
    

def mark_exception_on_display():
    global e_display
    
    e_display.Clear(0xff)
    e_display.fill(0xff)
    
    e_display.line(250, 70, 276, 70, 0x00)
    e_display.line(250, 70, 264, 50, 0x00)
    e_display.line(276, 70, 264, 50, 0x00)
    e_display.text("!", 260, 60, 0x00)
    e_display.display(e_display.buffer)
    
def add_IP_to_display(ip):
    global e_display
    
    e_display.text(ip, 100, 121, 0x00)
    update_display()
    
def update_date_on_display(weekday_number, date):
    global e_display
    
    e_display.fill_rect(210, 0, 86, 18, 0xff)
    
    weekday_str = weekday_str_list[weekday_number]
    e_display.text(weekday_str, 210, 0, 0x00)
    date_str = "{:02d}.{:02d}.{:d}".format(date[2], date[1], date[0])
    e_display.text(date_str, 210, 10, 0x00)
    update_display()
    
def set_value_to_buffer(value, x, y, float_number=True):
    global e_display
    
    value_str = ""
    if (float_number):
        value_str = "{:.1f}".format(value)
    else:
        value_str = "{:.0f}".format(value)
    e_display.fill_rect(x, y, 35, 10, 0xff)
    e_display.text(value_str, x, y, 0x00)
    
    
def update_display():
    global e_display
    
    e_display.display_Partial(e_display.buffer)
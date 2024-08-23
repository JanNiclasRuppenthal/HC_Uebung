from display.Pico_ePaper import EPD_2in9_Landscape
from util.config_date import weekday_str_list

class Display():
    
    def __init__(self):
        self.e_display = EPD_2in9_Landscape()
        
    def __set_title_station(self):
        self.e_display.text("Wetterstation", 5, 0, 0x00)
        self.e_display.text("Raspberry Pi Pico W", 5, 10, 0x00)
    
    def __set_title_temperature(self):
        temp_str = "Temperatur: "
        self.e_display.text(temp_str, 5, 50, 0x00)
        self.e_display.text("     Grad", 120, 50, 0x00)
        self.e_display.text("     Grad", 220, 25, 0x00)
        
    def __set_title_humidity(self):
        hum_str = "Feuchtigkeit: "
        self.e_display.text(hum_str, 5, 75, 0x00)
        self.e_display.text("     %", 120, 75, 0x00)
        self.e_display.text("     %", 220, 50, 0x00)
        self.e_display.text("     %", 220, 75, 0x00)
        
    def __set_title_ip(self):
        ip_str = "IP-Adresse: "
        self.e_display.text(ip_str, 5, 121, 0x00)
        
    def __set_initials(self):
        owner_str = "JNR#33"
        self.e_display.text(owner_str, 245, 121, 0x00)
        
    def __set_lines(self):
        self.e_display.hline(0, 20, 296, 0x00)
        self.e_display.hline(0, 115, 296, 0x00)
        self.e_display.vline(210, 20, 95, 0x00)
        

    def setup_display(self):
        self.e_display.Clear(0xff)
        self.e_display.fill(0xff)
        
        self.__set_title_station()
        self.__set_title_temperature()
        self.__set_title_humidity()
        self.__set_title_ip()
        self.__set_initials()
        self.__set_lines()
        
        # show result on display
        self.e_display.display(self.e_display.buffer)
        

    def mark_exception_on_display(self):
        self.e_display.Clear(0xff)
        self.e_display.fill(0xff)
        
        self.e_display.line(250, 70, 276, 70, 0x00)
        self.e_display.line(250, 70, 264, 50, 0x00)
        self.e_display.line(276, 70, 264, 50, 0x00)
        self.e_display.text("!", 260, 60, 0x00)
        self.e_display.display(self.e_display.buffer)
        
    def add_IP_to_display(self, ip):
        self.e_display.text(ip, 100, 121, 0x00)
        self.update_display()
        
    def update_date_on_display(self, weekday_number, date):
        self.e_display.fill_rect(210, 0, 86, 18, 0xff)
        
        weekday_str = weekday_str_list[weekday_number]
        self.e_display.text(weekday_str, 210, 0, 0x00)
        
        date_str = "{:02d}.{:02d}.{:d}".format(date[2], date[1], date[0])
        self.e_display.text(date_str, 210, 10, 0x00)
        
        self.update_display()
        
    def __set_value_to_buffer(self, value, x, y, float_number=True):
        value_str = ""
        
        if (float_number):
            value_str = "{:.1f}".format(value)
        else:
            value_str = "{:.0f}".format(value)
            
        self.e_display.fill_rect(x, y, 35, 10, 0xff)
        self.e_display.text(value_str, x, y, 0x00)
        
    def set_values_to_buffer(self, measure):
        self.__set_value_to_buffer(measure.temp_value, 120, 50)
        self.__set_value_to_buffer(measure.humi_value, 120, 75)
        self.__set_value_to_buffer(measure.temp_outdoor_value, 220, 25)
        self.__set_value_to_buffer(measure.humi_outdoor_value, 220, 50)
        self.__set_value_to_buffer(measure.light_outdoor_value, 220, 75)
        self.__set_value_to_buffer(measure.rain_outdoor_value, 220, 100, False)
           
        
    def update_display(self):
        self.e_display.display_Partial(self.e_display.buffer)

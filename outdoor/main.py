from machine import Pin, ADC
import time
import network
import socket
import select

from wifi_configuration import ssid, password

# Sensor-Pins
raindrop_sensor = Pin(16, Pin.IN)
photo_resistor = ADC(0)
led = Pin("LED", Pin.OUT)


UPDATE_RATE = 60

temp_value = -1
humi_value = -1
rain_value = -1
light_value = -1

count = -1

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

led.on()

while wlan.isconnected() == False:
    print('Verbinde mit dem WLAN...')
    time.sleep(1)

print('Mit WLAN verbunden, IP-Adresse:', wlan.ifconfig()[0])

ip = wlan.ifconfig()[0]

addr = (ip, 80)
connection = socket.socket()
connection.bind(addr)
connection.listen(1)

led.off()

def webpage(temp_value, humi_value, light_value, rain_value):
    html = f"""
<!DOCTYPE html>
<html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Wetterstation Raspberry Pi Pico W</title>
    </head>
    <body style="background-color:#121212EE;">

        <h1 style="text-align: center; color: white">Wetterdaten</h1>
        <h2 style="
                text-align: center; 
                margin-top: 5%; 
                margin-bottom: 5%;
                color: orange">Temperatur</h2>
        <div style="
                border: 1px solid #000000;
                background-color: aqua;
                padding: 5%;
                margin: 20px auto;
                width: 50%;
                text-align: center;
                border-radius: 12px;
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
                ">
                <p style="font-size:200%"><b>{temp_value}°C</b></p>
        </div>
        <h2 style="
                text-align: center; 
                margin-top: 5%; 
                margin-bottom: 5%;
                color: orange">Feuchtigkeit</h2>
        <div style="
                border: 1px solid #000000;
                background-color: aqua;
                padding: 5%;
                margin: 20px auto;
                width: 50%;
                text-align: center;
                border-radius: 12px;
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
                ">
                <p style="font-size:200%"><b>{humi_value}%</b></p>
        </div>
        <h2 style="
                text-align: center; 
                margin-top: 5%; 
                margin-bottom: 5%;
                color: orange">Lichtintensität</h2>
        <div style="
                border: 1px solid #000000;
                background-color: aqua;
                padding: 5%;
                margin: 20px auto;
                width: 50%;
                text-align: center;
                border-radius: 12px;
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
                ">
                <p style="font-size:200%"><b>{light_value}%</b></p>
        </div>
        <h2 style="
                text-align: center; 
                margin-top: 5%; 
                margin-bottom: 5%;
                color: orange">Regen</h2>
        <div style="
                border: 1px solid #000000;
                background-color: aqua;
                padding: 5%;
                margin: 20px auto;
                width: 50%;
                text-align: center;
                border-radius: 12px;
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
                ">
                <p style="font-size:200%"><b>{rain_value}</b></p>
        </div>
        <hr style="
                border-top: 3px solid darkviolet; 
                margin-top: 5%; 
                margin-bottom: 5%;">
    </body>
</html>
            """
    return str(html)

while True:
    if (count == -1 or count >= 2): #UPDATE_RATE * 60):
        
        # TODO: read the value from the delivered sensor
        temp_value = -1
        humi_value = -1
        rain_value = 1 if raindrop_sensor.value() == 0 else 0
        light = 65536 - photo_resistor.read_u16()
        
        # convert the value to %
        light_value = round((light / 65536) * 100, 1)

    time.sleep(1)
    count += 1

    try:
        ready_to_read, _, _ = select.select([connection], [], [], 1)
        if ready_to_read:
            led.on()
            conn, addr = connection.accept()
            request = conn.recv(1024)
            request = str(request)

            if '/temp_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{temp_value}"
            elif '/humi_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{humi_value}"
            if '/rain_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{rain_value}"
            elif '/light_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{light_value}"
            else:
                html_webpage = webpage(temp_value, humi_value, light_value, rain_value)
                response = "HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n" + html_webpage

            conn.send(response)
            conn.close()
            led.off()
        
    except OSError as e:
        machine.reset()

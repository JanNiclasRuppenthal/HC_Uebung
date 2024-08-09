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

# Webserver-Konfiguration
UPDATE_RATE = 10
count = -1

# WLAN verbinden
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140)
wlan.connect(ssid, password)

led.on()

while wlan.isconnected() == False:
    print('Verbinde mit dem WLAN...')
    time.sleep(1)

print('Mit WLAN verbunden, IP-Adresse:', wlan.ifconfig()[0])

ip = wlan.ifconfig()[0]

# Socket-Verbindung einrichten
addr = (ip, 80)
connection = socket.socket()
connection.bind(addr)
connection.listen(1)

print('Webserver gestartet, warte auf Anfragen...')

led.off()

# Haupt-Loop
while True:
    # Sensorwerte aktualisieren
    if (count == -1 or count >= 2): #UPDATE_RATE * 60):
        
        # Sensor-Werte lesen
        rain_value = 1 if raindrop_sensor.value() == 0 else 0
        light_value = 65536 - photo_resistor.read_u16()

    time.sleep(1)
    count += 1

    # Auf eingehende HTTP-Anfragen prüfen
    try:
        ready_to_read, _, _ = select.select([connection], [], [], 1)
        if ready_to_read:
            led.on()
            conn, addr = connection.accept()
            request = conn.recv(1024)
            request = str(request)

            # Auf spezifische Pfade prüfen
            if '/rain_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{rain_value}"
            elif '/light_value' in request:
                response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{light_value}"
            else:
                response = """HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nError 404: Not Found"""

            conn.send(response)
            conn.close()
            led.off()
        
    except OSError as e:
        pass

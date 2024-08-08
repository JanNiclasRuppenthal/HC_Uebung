import network
import socket
from time import sleep
import machine
from wifi.wifi_configuration import ssid, password

def connect_to_wifi():
    ip = connect()
    connection = open_socket(ip)
    return connection, ip
    

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for a connection to the wifi')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected to wifi with the following ip: {ip}')
    return ip
    
    
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection
    

def webpage(temperature, humidity, temp_queue, humi_queue):
    html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wetterstation Raspberry Pi Pico W</title>
    <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css">
    <script defer src="https://pyscript.net/latest/pyscript.js"></script>
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
        <p style="font-size:200%"><b>{temperature}°C</b></p>
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
        <p style="font-size:200%"><b>{humidity}%</b></p>
    </div>
    <hr style="
            border-top: 3px solid darkviolet; 
            margin-top: 5%; 
            margin-bottom: 5%;">
    <h1 style="text-align: center; color: white">Daten der letzten 24 Stunden</h1>
    <h2 style="
            text-align: center; 
            margin-top: 5%; 
            margin-bottom: 5%;
            color: orange">Temperatur</h2>
    <div id="output_temp" style="
            max-width: fit-content;
            margin-left: auto;
            margin-right: auto; 
            color: white";>Generiere ein Diagramm der letzten 24 Stunden...
    </div>
    <h2 style="
            text-align: center; 
            margin-top: 5%; 
            margin-bottom: 5%;
            color: orange">Feuchtigkeit</h2>
    <div id="output_humi" style="
            max-width: fit-content;
            margin-left: auto;
            margin-right: auto;
            color: white;">Generiere ein Diagramm der letzten 24 Stunden...
    </div>
    <hr style="
            border-top: 3px solid darkviolet; 
            margin-top: 5%; 
            margin-bottom: 5%;">
    <py-script>
        import micropip
        import asyncio
        import time

        async def main():
            await micropip.install('matplotlib')
            await micropip.install('numpy')
            
            import matplotlib.pyplot as plt
            from matplotlib.ticker import FormatStrFormatter
            import numpy as np

            # Daten generieren
            hour = time.localtime()[3]
            x = np.linspace(hour, hour+24, 144)
            
            plt.tight_layout()

            # Plot erstellen
            fig_temp, ax = plt.subplots(figsize=(4, 4))
            ax.plot(x, {temp_queue})
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            
            labels = [int((z % 24)) for z in ax.get_xticks()]
            ax.set_xticks(ax.get_xticks())
            ax.set_xticklabels([int((z % 24)) for z in ax.get_xticks()])
            ax.set(title='Temperatur', xlabel='Stunden', ylabel='°C')

            fig_humi, ax = plt.subplots(figsize=(4, 4))
            ax.plot(x, {humi_queue})
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            
            labels = [int((z % 24)) for z in ax.get_xticks()]
            ax.set_xticks(ax.get_xticks())
            ax.set_xticklabels([int((z % 24)) for z in ax.get_xticks()])
            ax.set(title='Feuchtigkeit', xlabel='Stunden', ylabel='%')

            # Plot im HTML-Dokument anzeigen
            from js import document
            import pyscript

            # Canvas-Element anpassen
            pyscript.write('output_temp', fig_temp)
            pyscript.write('output_humi', fig_humi)

        asyncio.ensure_future(main())
    </py-script>
</body>
</html>
            """
    return str(html)
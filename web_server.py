import network
import socket
from time import sleep
import machine
from wifi_configuration import ssid, password

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
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
    

def webpage(temperature, humidity):
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
    <h1 style="text-align: center; color: orange">Temperatur</h1>
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
    <h1 style="text-align: center; color: orange">Feuchtigkeit</h1>
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
    <div id="output" style="
              max-width: fit-content;
              margin-left: auto;
              margin-right: auto;">
    </div>
    <py-script>
        import micropip
        import asyncio

        async def main():
            await micropip.install('matplotlib')
            await micropip.install('numpy')
            import matplotlib.pyplot as plt
            import numpy as np

            # Daten generieren
            x = np.linspace(0, 10, 100)
            y = np.sin(x)

            # Plot erstellen
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.plot(x, y)
            ax.set(title='Sinusfunktion', xlabel='x', ylabel='sin(x)')

            # Plot im HTML-Dokument anzeigen
            from js import document
            import pyscript

            # Canvas-Element anpassen
            pyscript.write('output', fig)

        asyncio.ensure_future(main())
    </py-script>
</body>
</html>
            """
    return str(html)
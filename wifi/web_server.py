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
    

def webpage_indoor(temp_value, humi_value, temp_queue, humi_queue):
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
                text-align: center;
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
                text-align: center;
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
            from datetime import datetime, timedelta
            
            async def main():
                await micropip.install('matplotlib')
                await micropip.install('numpy')
                
                import matplotlib.pyplot as plt
                from matplotlib.dates import DateFormatter
                import numpy as np

                # x-Axis for the last 24 hours
                now = datetime.now()
                time_labels = [now - timedelta(minutes=i*10) for i in range((60//10) * 24)]
                time_labels.reverse()
                
                def create_plot(queue, title, ylabel):
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.plot(time_labels, queue)
                    ax.set(title=title, xlabel='Zeit', ylabel=ylabel)
                    ax.xaxis.set_major_formatter(DateFormatter('%H'))
                    fig.autofmt_xdate()
                    
                    return fig

                # Canvas-Element anpassen
                Element('output_temp').write(create_plot({temp_queue},'Temperatur', '°C'))
                Element('output_humi').write(create_plot({humi_queue}, 'Feuchtigkeit', '%'))
            asyncio.ensure_future(main())
        </py-script>
    </body>
</html>

            """
    return str(html)


def webpage_outdoor(temp_value, humi_value, light_value, rain_value):
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
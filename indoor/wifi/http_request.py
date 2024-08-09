import socket
from wifi_configuration import server_ip

# Funktion zum Abrufen von Daten
def get_outdoor_sensor_value(request):
    addr = (server_ip, 80)
    s = socket.socket()
    s.connect(addr)
    get_request = f"GET {request} HTTP/1.1\r\nHost: {server_ip}\r\nConnection: close\r\n\r\n"
    s.send(get_request.encode())

    response_bytes = b""
    response_bytes = b"" + s.recv(4096)
    s.close()
    
    response_str = response_bytes.decode('utf-8')
    index_to_value = response_str.rfind('\n') + 1
    value = int(response_str[index_to_value:])
    
    return value
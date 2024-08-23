import socket
from wifi.wifi_configuration import server_ip

def __convert_response_to_value(response_bytes):
    response_str = response_bytes.decode('utf-8')
    index_to_value = response_str.rfind('\n') + 1
    value = round(float((response_str[index_to_value:])), 1)
    
    return value

def get_outdoor_sensor_value(request):
    addr = (server_ip, 80)
    s = socket.socket()

    # Test if the other station is reachable
    try:
        s.connect(addr)
    except OSError as e:
        s.close()
        return -1
    
    get_request = f"GET {request} HTTP/1.1\r\nHost: {server_ip}\r\nConnection: close\r\n\r\n"
    s.send(get_request.encode())

    response_bytes = b""
    response_bytes = b"" + s.recv(4096)
    s.close()

    return __convert_response_to_value(response_bytes)
    
import socket
import ssl
from urllib.parse import urlparse



def http_get(url):


    default_headers = {
        'User_Agent': 'Chrome 200/Mozila 900 Codemate TV Amir',
        'Content-Type': 'application/json',
        'accept':'\*'
    }

    parsed_url = urlparse(url)

    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'
    scheme = parsed_url.scheme
    port = 443 if scheme =='https' else 80


    #create TCP/IP

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:

        if scheme == 'http':
            sock.connect((host,port))

            headers = '\r\n'.join([f"{key}: {value}" for key,value in default_headers.items()])
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n{headers}\r\nConnection: close\r\n\r\n"
            sock.sendall(request.encode())

            response = b""

            while 1:
                data = sock.recv(4096)
                if not data:
                    break
                response+= data
            
        elif scheme == 'https':
            context = ssl.create_default_context()
            with context.wrap_socket(sock,server_hostname=host) as s:
                s.connect((host,port))
                headers = '\r\n'.join([f"{key}: {value}" for key,value in default_headers.items()])
                request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n{headers}\r\nConnection: close\r\n\r\n"
                s.sendall(request.encode())
                response = b""

                while 1:
                    data = s.recv(4096)
                    if not data:
                        break
                    response+= data

            
    header_data, body = response.split(b'\r\n\r\n',1)

    return header_data.decode(), body.decode()



url = 'http://httpbin.org/get'

headers, body = http_get(url)
print("Response Headers:")
print(headers)
print("\nBody: ")
print(body)


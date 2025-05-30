import socket
import select
import sys
import os

server_address = ('localhost', 8080)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        #read_ready,write_ready,exception
        read_ready, _, _ = select.select(input_socket, [], [])
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                # receive data from client, break when null received
                data = sock.recv(4096)
                if data:
                    data = data.decode()
                    request_header = data.split('\r\n')
                    print('Request header:', request_header)
                    request_file = request_header[0].split()[1]

                    if request_file in ('/', '/index.html'):
                        try:
                            with open('index.html', 'r') as f:
                                response_data = f.read()
                            content_length = len(response_data.encode())
                            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {content_length}\r\n\r\n'
                            sock.sendall(response_header.encode() + response_data.encode())
                        except FileNotFoundError:
                            sock.sendall(b'HTTP/1.1 404 Not Found\r\n\r\nFile Not Found')
                    else:
                        sock.sendall(b'HTTP/1.1 404 Not Found\r\n\r\nInvalid Path')
                else:
                    input_socket.remove(sock)
                    sock.close()
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)

import socket

def get_first_length(data):
    header = data.split('\r\n\r\n')[0]
    header_length = len(header)
    content_length = 0
    for line in header.split('\r\n'):
        if line.lower().startswith('content-length:'):
            parts = line.split(':', 1)
            if len(parts) == 2:
                try:
                    content_length = int(parts[1].strip())
                except ValueError:
                    return 0
    return header_length + content_length

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8080)
client_socket.connect(server_address)

# Send request for /index.html
request_header = b'GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n'
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    decoded_received = received.decode('utf-8')
    response += decoded_received

    # Optional: break early if length check succeeds
    if get_first_length(response) <= len(response):
        break

print(response)
client_socket.close()

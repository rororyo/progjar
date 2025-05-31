import socket
import ssl
from io import StringIO
import unittest
from unittest.mock import MagicMock, patch
import json
import sys
data = {"name": "John Doe", "age": 30}
host = 'httpbin.org'
port = 443
context = ssl.create_default_context()
#Serialize json
content = json.dumps(data)
content_length = len(content)

# Create connection
plain_socket = socket.create_connection((host, port))
ssl_socket = context.wrap_socket(plain_socket, server_hostname=host)
#Build Request Header
request_header = (
    "POST /post HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Content-Type: application/json\r\n"
    f"Content-Length: {content_length}\r\n"
    "Connection: close\r\n\r\n"
)
ssl_socket.sendall(request_header.encode()+content.encode( ))

response = ssl_socket.recv(1024)
ssl_socket.close()
response_text = response.decode()
parts = response_text.split('\r\n\r\n', 1)
print(parts[0])


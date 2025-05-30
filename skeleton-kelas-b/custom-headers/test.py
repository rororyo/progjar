import socket
import ssl
import sys
from io import StringIO
import unittest
from unittest.mock import MagicMock, patch
import json

host = 'httpbin.org'
port = 443
context = ssl.create_default_context()
plain_socket = socket.create_connection((host, port))
ssl_socket = context.wrap_socket(plain_socket,server_hostname=host)
request_header = (
    "GET /headers HTTP/1.1\r\n"
    "Host: httpbin.org\r\n"
    "X-Test-Header: TestValue\r\n"
    "Connection: close\r\n\r\n"
)
ssl_socket.send(request_header.encode())
response = b''
while True:
    chunk = ssl_socket.recv(4096)
    if not chunk:
        break
    response += chunk

ssl_socket.close()
response_text = response.decode()
parts = response_text.split('\r\n\r\n', 1)
if len(parts) < 2:
    print("Error: No response body found")
    sys.exit(1)

body = parts[1]
print(body)
json_body =json.loads(body)
print(json_body)
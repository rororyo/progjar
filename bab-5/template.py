from unittest.mock import patch, MagicMock
import socket
import json
from io import StringIO
import unittest
import sys
from unittest import mock
from urllib.parse import urlencode

#Get request
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = 'jsonplaceholder.typicode.com'
    port = 80
    s.connect((host,port))
        # Prepare HTTP request with custom header
    request = (
        "GET /posts HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Connection: close\r\n\r\n"
    )
    s.send(request.encode())
    
    #Receive response
    response = s.recv(4096)
    response_text = response.decode()
    parts = response_text.split('\r\n\r\n',1)
    body = parts[1]
    body_json = ''
    occurence= 0
    s.close()
    if "6b80[" in body and body.endswith('0'):
        json_str = body.split('[', 1)[1].rsplit(']', 1)[0]
        json_str = '[' + json_str + ']'
        body_json = json.loads(json_str)
    for item in body_json:
        if word in item['body']:
            occurence += 1

#Post request
host = 'jsonplaceholder.typicode.com'
port = 80

# Serialize json
content = json.dumps({
    "title":title,
    "body":body,
    "userId":user_id
})
content_length = len(content)

# Create connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to the server
    sock.connect((host, port))
    
    # Build Request Header
    request_header = (
        "POST /posts HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {content_length}\r\n"
        "Connection: close\r\n\r\n"
    )
            # Send the request header and content
    sock.send((request_header + content).encode())

    # Receive all data
    response = sock.recv(4096)
    response_text = response.decode()
    parts = response_text.split('\r\n\r\n', 1)
    body = parts[1]
    body_json = json.loads(body)
    return body_json['id']
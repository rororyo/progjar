from unittest.mock import patch, MagicMock
import socket
import json
from io import StringIO
import unittest
import sys
from unittest import mock
from urllib.parse import urlencode
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = 'jsonplaceholder.typicode.com'
    port = 80
    s.connect((host,port))
        # Prepare HTTP request with custom header
    request = (
        "GET /comments?postId=1 HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Connection: close\r\n\r\n"
    )
    s.send(request.encode())
    
    #Receive response
    response = s.recv(4096)
    response_text = response.decode()
    parts = response_text.split('\r\n\r\n',1)
    body = parts[1]
    # body_json = json.load(body)
if "5e6\r\n[" in body:
    json_str = body.split('[', 1)[1].rsplit(']', 1)[0]
    json_str = '[' + json_str + ']'
    body_json = json.loads(json_str)
    print(len(body_json))

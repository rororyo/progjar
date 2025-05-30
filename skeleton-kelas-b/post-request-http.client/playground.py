from unittest.mock import patch, MagicMock
import socket
import json
from io import StringIO
import unittest
import sys
import http.client

connection = http.client.HTTPSConnection("jsonplaceholder.typicode.com")
body = json.dumps({
    "postId":1,
    "name":"Test Name",
    "email":"test@example.com"
    })
connection.request("POST", "/comments",body)
response = connection.getresponse()
response_body = response.read().decode()
response_json = json.loads(response_body)
print(response_json['id'])

connection.close()
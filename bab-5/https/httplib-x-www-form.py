from unittest.mock import patch, MagicMock
import socket
import json
from io import StringIO
import unittest
import sys
import http.client
from unittest import mock
from urllib.parse import urlencode


def post_comment():
    connection = http.client.HTTPSConnection("jsonplaceholder.typicode.com")

    body = urlencode({
        "postId": 1,
        "name": "Test Name",
        "email": "test@example.com",
        "body": "This is a test comment."
    })

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    connection.request("POST", "/comments", body=body, headers=headers)
    response = connection.getresponse()
    response_body = response.read().decode()
    response_json = json.loads(response_body)
    connection.close()

    return response_json['id']
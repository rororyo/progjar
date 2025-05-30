from unittest.mock import patch, MagicMock
import socket
import ssl
import json
from io import StringIO
import unittest
import sys

def get_custom_header():
    host = 'httpbin.org'
    port = 443
    context = ssl.create_default_context()
    plain_socket = socket.create_connection((host, port))
    ssl_socket = context.wrap_socket(plain_socket, server_hostname=host)
#X Test header is custom header
    request_header = (
        "GET /headers HTTP/1.1\r\n"
        "Host: httpbin.org\r\n"
        "X-Test-Header: TestValue\r\n"
        "Connection: close\r\n\r\n"
    )
    ssl_socket.send(request_header.encode())

    response = b""
    while True:
        data = ssl_socket.recv(4096)
        if not data:
            break
        response += data

    ssl_socket.close()

    response_text = response.decode()
    body = response_text.split('\r\n\r\n', 1)[1]
    json_body = json.loads(body)
    return json_body["headers"].get("X-Test-Header")


class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestHeaderRequester(unittest.TestCase):
    @patch('socket.create_connection')
    @patch('ssl.create_default_context')
    def test_get_custom_header(self, mock_ssl_context, mock_create_connection):
        mock_plain_socket = MagicMock()
        mock_ssl_socket = MagicMock()

        # Mock socket.create_connection
        mock_create_connection.return_value = mock_plain_socket

        # Mock ssl.wrap_socket
        mock_context_instance = MagicMock()
        mock_ssl_context.return_value = mock_context_instance
        mock_context_instance.wrap_socket.return_value = mock_ssl_socket

        # Mock response
        fake_response = (
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
            "{\"headers\": {\"X-Test-Header\": \"TestValue\"}}"
        ).encode()
        mock_ssl_socket.recv.side_effect = [fake_response, b'']

        # Run
        result = get_custom_header()

        # Assertions
        mock_create_connection.assert_called_with(('httpbin.org', 443))
        print(f"connect called with: {mock_create_connection.call_args}")

        mock_ssl_socket.send.assert_called_once()
        print(f"send called with: {mock_ssl_socket.send.call_args}")

        print(f"recv called with: {mock_ssl_socket.recv.call_args_list}")

        assert_equal(result, "TestValue")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        header_field = get_custom_header()
        print(header_field)

    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)

import socket
import ssl
from io import StringIO
import unittest
from unittest.mock import MagicMock, patch
import json
import sys

def post_data(data):
    host = 'httpbin.org'
    port = 80
    
    # Serialize json
    content = json.dumps(data)
    content_length = len(content)

    # Create connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to the server
        sock.connect((host, port))
        
        # Build Request Header
        request_header = (
            "POST /post HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {content_length}\r\n"
            "Connection: close\r\n\r\n"
        )
        
        # Send the request header and content
        sock.send((request_header + content).encode())

        # Receive all data
        response = b""
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            response += chunk

    response_text = response.decode()
    parts = response_text.split('\r\n\r\n', 1)
    if len(parts) < 2:
        print("len < 2")
        body = ''
    else:
        body = parts[1]
    return body


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestPostData(unittest.TestCase):
    @patch('socket.socket')
    def test_post_data(self, mock_socket):
        # Setup the mocked socket instance
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance

        # Define the mock response from the server
        response_body = {"received": "ok", "status": "success"}
        http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "\r\n"
            "{}".format(len(json.dumps(response_body)), json.dumps(response_body))
        )
        mock_sock_instance.recv.side_effect = [http_response.encode('utf-8'), b'']

        # Call the function
        data = {"name": "John Doe", "age": 30}
        body = post_data(data)

        # Assertions to check if the response body is correctly returned
        mock_sock_instance.connect.assert_called_once_with(('httpbin.org', 80))
        print(f"connect called with: {mock_sock_instance.connect.call_args}")

        mock_sock_instance.send.assert_called_once()
        print(f"send called with: {mock_sock_instance.send.call_args}")

        mock_sock_instance.recv.assert_called()
        print(f"recv called with: {mock_sock_instance.recv.call_args}")

        assert_equal(body, json.dumps(response_body))


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        data = {"name": "John Doe", "age": 30}
        return_data = post_data(data)
        print(return_data)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
    # unittest.main(exit=False)
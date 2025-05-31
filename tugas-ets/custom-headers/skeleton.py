import socket
from io import StringIO
import unittest
from unittest.mock import MagicMock, patch
import json
import sys

def get_custom_header():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('httpbin.org', 80))
        
        # Prepare HTTP request with custom header
        request = (
            "GET /headers HTTP/1.1\r\n"
            "Host: httpbin.org\r\n"
            "X-Test-Header: TestValue\r\n"
            "Connection: close\r\n\r\n"
        )
        
        # Send the request
        s.send(request.encode())
        
        # Receive the response
        response = s.recv(4096)
        
        # Decode the response
        response_text = response.decode('utf-8')
        
        # Find the JSON part of the response
        body = response_text.split('\r\n\r\n', 1)[1]
        
        # Parse the JSON
        try:
            response_json = json.loads(body)
            # Extract the header value
            return response_json["headers"]["X-Test-Header"]
        except (json.JSONDecodeError, KeyError):
            return None

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestHeaderRequester(unittest.TestCase):
    @patch('socket.socket')
    def test_get_custom_header(self, mock_socket):
        # Setup the mock socket
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        
        # Define a fake response to be returned by socket.recv
        fake_response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"headers\": {\"X-Test-Header\": \"TestValue\"}}"
        mock_socket_instance.recv.return_value = fake_response.encode()

        # Call the function
        test_header_value = get_custom_header()

        # Verify that the socket methods were called correctly
        mock_socket_instance.connect.assert_called_with(('httpbin.org', 80))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")

        mock_socket_instance.send.assert_called_once()
        print(f"send called with: {mock_socket_instance.send.call_args}")

        mock_socket_instance.recv.assert_called_once()
        print(f"recv called with: {mock_socket_instance.recv.call_args}")

        assert_equal(test_header_value, "TestValue")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        header_field = get_custom_header()
        print(header_field)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)

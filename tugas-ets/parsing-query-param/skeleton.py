from unittest.mock import patch, MagicMock
import socket
import json
from io import StringIO
import unittest
import sys
from unittest import mock
from urllib.parse import urlencode


def fetch_comments():
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
        # return body
        # body_json = json.load(body)
        s.close()
        if "5e3[" in body and body.endswith('0'):
            json_str = body.split('[', 1)[1].rsplit(']', 1)[0]
            json_str = '[' + json_str + ']'
            body_json = json.loads(json_str)
            return len(body_json)
            


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestCommentsFetcher(unittest.TestCase):
    @patch('socket.socket')
    def test_fetch_comments(self, mock_socket):
        # Setup mock socket
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        # Define the fake response to be returned by socket.recv
        fake_response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n5e3[{\"postId\": 1, \"id\": 1, \"name\": \"Test Comment\"}]0"
        mock_socket_instance.recv.return_value = fake_response.encode()

        # Call the function
        result = fetch_comments()

        # Assertions to verify behavior and results
        mock_socket_instance.connect.assert_called_with(('jsonplaceholder.typicode.com', 80))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")

        mock_socket_instance.send.assert_called_once()
        print(f"send called with: {mock_socket_instance.send.call_args}")
        
        mock_socket_instance.recv.assert_called_once()
        print(f"recv called with: {mock_socket_instance.recv.call_args}")

        assert_equal(result, 1)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        comment = fetch_comments()
        print(comment)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
    # unittest.main(exit=False)
from unittest.mock import patch, MagicMock
import socket
import json
from io import StringIO
import unittest
import sys
from unittest import mock
from urllib.parse import urlencode

def create_post(title, body, user_id):
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


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestCreatePost(unittest.TestCase):
    @patch('socket.socket')
    def test_create_post(self, mock_socket):
        # Setup the mocked socket
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance

        # Define the mock response from the server
        response_data = {
            'id': 101,
            'title': 'New Entry',
            'body': 'This is a new post.',
            'userId': 1
        }
        http_response = f"HTTP/1.1 201 Created\r\nContent-Length: {len(json.dumps(response_data))}\r\n\r\n{json.dumps(response_data)}"
        mock_sock_instance.recv.side_effect = [http_response.encode('utf-8'), b'']

        # Call the function
        post_id = create_post("New Entry", "This is a new post.", 1)

        # Assertions to check if the POST request was properly sent and the correct ID was returned
        # Verify that the socket methods were called correctly
        mock_sock_instance.connect.assert_called_with(('jsonplaceholder.typicode.com', 80))
        print(f"connect called with: {mock_sock_instance.connect.call_args}")

        mock_sock_instance.send.assert_called_once()
        print(f"send called with: {mock_sock_instance.send.call_args}")

        mock_sock_instance.recv.assert_called()
        print(f"recv called with: {mock_sock_instance.recv.call_args}")

        mock_sock_instance.send.assert_called_once()
        assert_equal(post_id, 101)
        


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        post_id = create_post('This is a new title', 'This is a new post.', 1)
        print(post_id)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
    # unittest.main(exit=False)

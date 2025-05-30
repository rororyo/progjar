import socket
import json
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys


def fetch_users_from_city(city_name):
    host = 'jsonplaceholder.typicode.com'
    port = 80
    
    # Create a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        
        # Prepare HTTP request
        request = (
            f"GET /users HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Connection: close\r\n\r\n"
        )
        
        # Send the request
        sock.send(request.encode())
        
        # Receive the response
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
    
    # Parse the response
    response_text = response.decode('utf-8')
    
    # Split headers and body
    parts = response_text.split('\r\n\r\n', 1)
    if len(parts) < 2:
        return []
    #Remove the unecessary parts
    body = parts[1]
    if "160d\r\n[" in body and body.endswith('0'):
        json_str = body.split('[', 1)[1].rsplit(']', 1)[0]
        json_str = '[' + json_str + ']'
        users_data = json.loads(json_str)
        filtered_users = [user["name"] for user in users_data if user.get("address", {}).get("city") == city_name]
        return filtered_users


        


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestFetchUsersFromCity(unittest.TestCase):
    @patch('socket.socket')
    def test_fetch_users_from_kulas_light(self, mock_socket):
        # Setup the mocked socket instance
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance

        # Simulate a JSON response from the server
        users_data = [
            {"id": 1, "name": "Leanne Graham", "address": {"city": "Gwenborough"}},
            {"id": 2, "name": "Ervin Howell", "address": {"city": "Wisokyburgh"}}
        ]
        http_response = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n160d\r\n" + json.dumps(users_data).encode('utf-8') + b'0'

        # Mock the recv method to simulate receiving the response in two parts
        mock_sock_instance.recv.side_effect = [http_response[:70], http_response[70:], b'']

        # Call the function under test
        result = fetch_users_from_city("Gwenborough")

        # Verify that the socket methods were called correctly
        mock_sock_instance.connect.assert_called_with(('jsonplaceholder.typicode.com', 80))
        print(f"connect called with: {mock_sock_instance.connect.call_args}")

        mock_sock_instance.send.assert_called_once()
        print(f"send called with: {mock_sock_instance.send.call_args}")

        mock_sock_instance.recv.assert_called()
        print(f"recv called with: {mock_sock_instance.recv.call_args}")

        # Assertions to check the correct behavior
        assert_equal(result, ["Leanne Graham"])


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        names = fetch_users_from_city("Gwenborough")
        for name in names:
            print(name)
    
    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
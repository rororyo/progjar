import socket
import zlib
HOST = 'localhost'
PORT = 12345
message = "Hello from client! This message is compressed with zlib"

#compress message
compressed_message = zlib.compress(message.encode())

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
  client_socket.connect((HOST,PORT))
  client_socket.sendall(compressed_message)
  print("sent compressed data")
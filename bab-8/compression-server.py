import socket
import zlib

HOST = 'localhost'
PORT = 12345

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
  server_socket.bind((HOST,PORT))
  server_socket.listen()
  print(f'server listening on {HOST}:{PORT}')

  conn,addr = server_socket.accept()
  with conn:
    print(f"Connected by {addr}")
    compressed_data = conn.recv(1024)

    # Decompress the data using zlib
    try:
      decompressed_data = zlib.decompress(compressed_data)
      print("Received(decompressed):", decompressed_data.decode())
    except zlib.error as e:
      print("Decompression error",e)
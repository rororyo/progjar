import socket

server_address = ('127.0.0.1',5001)
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.connect(server_address)

message= b'Hi ...'
delay = 2

while True:
  client_socket.send(message)
  client_socket.settimeout(delay)
  try:
    recv_message = client_socket.recv(1024)
    print(recv_message, 'delay: ',delay)
  except socket.timeout:
    delay *=2
    if delay > 4:
      print('server is down')
    else:
      break
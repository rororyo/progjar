import socket
import ssl
import gzip
from io import BytesIO
from bs4 import BeautifulSoup

#Define hostname and ssl context
hostname = 'www.python.org'
context = ssl.create_default_context()

#Create an SSL socket connection
with socket.create_connection((hostname,443)) as sock:
  with context.wrap_socket(sock,server_hostname=hostname) as csock:
    #Create request header
    request_header = f"GET / HTTP/1.1\r\nHost:{hostname}\r\nAccept-Encoding: gzip\r\nConnection: close\r\n\r\n"
    csock.send(request_header.encode())

    #Initialize buffer for response
    response = bytearray()
    try:
      while True: 
        chunk = csock.recv(1024)
        if not chunk:
          break
        response+=chunk
    except socket.timeout:
      print("Connection timed out")
    #Parse response into header and content
    print(response.decode())
    #seperate header with content
    header,_,content = response.partition(b'\r\n\r\n')
    if 'gzip' in header.decode():
      buf = BytesIO(content)
      f = gzip.GzipFile(fileobj=buf)
      content = f.read()
      soup = BeautifulSoup(content.decode('utf-8', errors='replace'), 'lxml')
      print(soup.get_text())

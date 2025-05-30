import socket
import time
import sys
import pickle
import json

def now():
  return time.asctime(time.localtime(time.time()))

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',5001))

while 1:
  try:
    msg = []
    msg.append("Hi server")
    msg.append(now())
    msg_dict = {
      'message' : 'Hi Server',
      'timestamp': now()
    }
    #using pickle
    # msg = pickle.dumps(msg)
    # s.send(msg)
    #using json
    msg_dict = bytes(json.dumps(msg_dict),'utf-8')
    s.send(msg_dict)
    time.sleep(1)
  except(KeyboardInterrupt,SystemExit):
    s.close()
    sys.exit(0)
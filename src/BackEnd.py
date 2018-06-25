#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================

import json
from thread import *
import threading
import socket

timeDiff = 0

def updateDataJSON(data):
    with open('dos_data.json', 'w') as fp:
        json.dump(data, fp, indent=4)

def getDataJSON():
    with open('dos_data.json', 'r') as fp:
        data = json.load(fp)
    return data
   
def getTimeDiff():
    return timeDiff
   
def Backend_socket(num1):
    print "Starting Backend_socket"
    try:
        HOST = ''  # Symbolic name meaning the local host
        PORT = 5000  # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print 'Connected by', addr
        data = conn.recv(1024)
        global timeDiff
        timeDiff = int(data)
    except:
        print 'Unable to connect Backend Socket listener'
 
if __name__ == '__main__':
    start_new_thread(Backend_socket, (1,))
  
 

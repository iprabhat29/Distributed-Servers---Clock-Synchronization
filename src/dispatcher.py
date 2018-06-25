#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================

import time
import threading
import socket
from thread import *
from Queue import Queue
ThreadLock = threading.Lock()
cv = threading.Condition()
import re
import requests
from api import api as api_back
from api2 import api as api_f2
from api1 import api as api_f1
from restart.serving import Service
from random import *

# This function creates REST API server for each client which connects
service = Service(api_back)
service1 = Service(api_f1)
service2 = Service(api_f2)


def startserver(num):
    # print "RUNNIN SERVER REST--->"
    service.run(port=5000)
    
    return
def startserver1(num):
    # print "RUNNIN SERVER REST--->"
    
    service1.run(port=9090)
    return

def startserver2(num):
    # print "RUNNIN SERVER REST--->"
    
    service2.run(port=9092)
    return

def FEP1_socket(num1):
  print "Starting FEP1 Socket"
  HOST = ''  # Symbolic name meaning the local host
  PORT = 9091  # Arbitrary non-privileged port
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  s.listen(1)
  conn, addr = s.accept()
  print 'Connected by', addr

"""def FEP1_socket(num1):
  print "Starting FEP1 Socket"
  host = ""
  port = 9092
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((host, port))
  s.listen(5)
  print "FEP1 Listning on ",port
  while(True):
    c,addr = s.accept()
    data = c.recv(1024)
    if data:
      print data
      ok = "OK"
      c.send(ok.encode('ascii'))

"""
def FEP1_Berk_socket(num1):

  
    print "Starting FEP1 Socket"
    HOST = ''  # Symbolic name meaning the local host
    PORT = 9091  # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
  
def FEP2_Berk_socket(num1):
    print "Starting FEP2 Socket"
    HOST = ''  # Symbolic name meaning the local host
    PORT = 9092  # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr

def castVoteFEP1():
    start_new_thread(FEP1_Berk_socket, (1,))
    start_new_thread(FEP2_Berk_socket, (1,))
    
    name = 'Fep_1_Server'
    id = random.randint(1, 10)
    vote = name + ':' + str(id) + ','
    url = "http://127.0.0.1:9092/castVote/" + str(vote)
    # print "Sending Reuest ",url
    requests.put(url)
 
 
def FEP2_socket(num1):
 print "Starting FEP2 Socket"
 HOST = ''  # Symbolic name meaning the local host
 PORT = 9092  # Arbitrary non-privileged port
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.bind((HOST, PORT))
 s.listen(1)
 conn, addr = s.accept()
 print 'Connected by', addr


def Winner(num):
  print "Starting raffle winner"
  count = 0
  while True:
    cv.acquire()
    if len(RaffleWinner) == 10 and count == 0:
      x = randint(0, 9)
      print "And the WINNER is--------->", RaffleWinner[x]
      count = 1
      cv.notify_all()

    else:
      cv.wait()
    cv.release()


def RaffleLottery(num):
  print "Starting Raffle Lottery"
  count = 0
  while True:
    cv.acquire()
    if (len(RaffleList) == 100 and count == 0):
      print "100th client --------------------------------------------->", RaffleList[99]
      RaffleWinner.append(RaffleList[99])
      # count = 1
      cv.notify_all()
    elif (len(RaffleList) == 200 and count == 1):
      print "200th client --------------------------------------------->", RaffleList[199]
      RaffleWinner.append(RaffleList[199])
      # count = 2
      cv.notify_all()
    elif (len(RaffleList) == 300 and count == 2):
      print "300th client --------------------------------------------->", RaffleList[299]
      RaffleWinner.append(RaffleList[299])
      # count = 3
      cv.notify_all()
    elif (len(RaffleList) == 400 and count == 3):
      print "400th client --------------------------------------------->", RaffleList[399]
      RaffleWinner.append(RaffleList[399])
      # count = 4
      cv.notify_all()
    elif (len(RaffleList) == 500 and count == 4):
      print "500th client --------------------------------------------->", RaffleList[499]
      RaffleWinner.append(RaffleList[499])
      # count = 5
      cv.notify_all()
    else:
      cv.wait()
    cv.release()

def EndServer(data):
  # return data + " will be sent"
  data_temp = re.sub('[^A-Za-z0-9]+', '', data)
  if 'incrementMedalTally' in data_temp:
    url = "http://127.0.0.1:5000" + str(data)
    # print "Sending Reuest ",url
    data1 = requests.put(url).json()
  elif 'getMedalTally' in data_temp:
    url = "http://127.0.0.1:5000" + str(data)
    # print "Sending Request ",url
    data1 = requests.get(url).json()
  elif 'pushUpdate' in data_temp:
    url = "http://127.0.0.1:5000" + str(data)
    # print "Sending Request ",url
    data1 = requests.put(url)
  elif 'setScore' in data_temp:
    url = "http://127.0.0.1:5000" + str(data)
    # print "Sending request ",url
    data1 = requests.put(url).json()
    # print "Set Score",data1
  elif 'registerClient' in data_temp:
    url = "http://127.0.0.1:5000" + str(data)
    # print "Sending Request ",url
    data1 = requests.put(url)
  elif 'getScore' in data_temp:
    url = "http://127.0.0.1:5000" + str(data)
    # print "Sending Request ",url
    data1 = requests.get(url).json()
  return data1  

    
def FEP1(num):

  #=============================================================================
  # Code Beginning for Berkeley Clock Synchronization algorithm
  #=============================================================================

  castVoteFEP1()
  #=============================================================================
  # -------
  #=============================================================================

  print "Starting FEP1"
  start_new_thread(FEP1_socket, (1,))
  time.sleep(2)
  HOST = ''  # The remote host
  PORT = 9092  # The same port as used by the server
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))
  while True:
    cv.acquire()
    if FEP1Queue.qsize() != 0:
      c = FEP1Queue.get()
      # print "FEP1 RECEIVING DATA"
      data = c.recv(1024)
      data_temp = re.sub('[^A-Za-z0-9]+', '', data)
      # print data_temp
      if 'Client' in data_temp:
        # print data_temp
        RaffleList.append(data_temp)
        
        if (len(RaffleList) == 100):
          print "100th client --------------------------------------------->", RaffleList[99]
          RaffleWinner.append(RaffleList[99])
          # count = 1
          # cv.notify_all()
        elif (len(RaffleList) == 200):
          print "200th client --------------------------------------------->", RaffleList[199]
          RaffleWinner.append(RaffleList[199])
          # count = 2
          # cv.notify_all()
        elif (len(RaffleList) == 300):
          print "300th client --------------------------------------------->", RaffleList[299]
          RaffleWinner.append(RaffleList[299])
          # count = 3
          # cv.notify_all()
        elif (len(RaffleList) == 400):
          print "400th client --------------------------------------------->", RaffleList[399]
          RaffleWinner.append(RaffleList[399])
          # count = 4
          # cv.notify_all()
        elif (len(RaffleList) == 500):
          print "500th client --------------------------------------------->", RaffleList[499]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        elif (len(RaffleList) == 600):
          print "600th client --------------------------------------------->", RaffleList[599]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        elif (len(RaffleList) == 700):
          print "700th client --------------------------------------------->", RaffleList[699]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        elif (len(RaffleList) == 800):
          print "800th client --------------------------------------------->", RaffleList[799]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        elif (len(RaffleList) == 900):
          print "900th client --------------------------------------------->", RaffleList[899]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        elif (len(RaffleList) == 1000):
          print "1000th client --------------------------------------------->", RaffleList[999]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        # else:
          # RaffleList.append(data_temp)

      result = "0"
      c.send("Done")
      
      while True:
        data = c.recv(1024)
        # print "FEP1 sending data to end server---",data
        if data:
          result = EndServer(data)
          c.send(result)
        else:
          break
      
      cv.notify_all()
    
    else:
      cv.wait()
    
    cv.release()


def FEP2(num):
  
  print "Starting FEP2"
  start_new_thread(FEP2_socket, (1,))
  time.sleep(2)
  HOST = ''  # The remote host
  PORT = 9091  # The same port as used by the server
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))

  while True:
    cv.acquire()
    if FEP2Queue.qsize() != 0:
      c = FEP2Queue.get()
      # ackMsg = "ACK"
      # f.send(ackMsg.encode('ascii'))
      # print "FEP2 RECEIVING DATA"
      data = c.recv(1024)
      data_temp = re.sub('[^A-Za-z0-9]+', '', data)
      if 'Client' in data_temp:
        # f.send(ackMsg.encode('ascii'))
        # f.send(data_temp.encode('ascii'))
        RaffleList.append(data_temp) 
        # print data_temp
        if (len(RaffleList) == 100):
          print "100th client --------------------------------------------->", RaffleList[99]
          RaffleWinner.append(RaffleList[99])
          # count = 1
          # cv.notify_all()
        elif (len(RaffleList) == 200):
          print "200th client --------------------------------------------->", RaffleList[199]
          RaffleWinner.append(RaffleList[199])
          # count = 2
          # cv.notify_all()
        elif (len(RaffleList) == 300):
          print "300th client --------------------------------------------->", RaffleList[299]
          RaffleWinner.append(RaffleList[299])
          # count = 3
          # cv.notify_all()
        elif (len(RaffleList) == 400):
          print "400th client --------------------------------------------->", RaffleList[399]
          RaffleWinner.append(RaffleList[399])
          # count = 4
          # cv.notify_all()
        elif (len(RaffleList) == 500):
          print "500th client --------------------------------------------->", RaffleList[499]
          RaffleWinner.append(RaffleList[499])
        elif (len(RaffleList) == 600):
          print "600th client --------------------------------------------->", RaffleList[599]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        elif (len(RaffleList) == 700):
          print "700th client --------------------------------------------->", RaffleList[699]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        elif (len(RaffleList) == 800):
          print "800th client --------------------------------------------->", RaffleList[799]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        elif (len(RaffleList) == 900):
          print "900th client --------------------------------------------->", RaffleList[899]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        elif (len(RaffleList) == 1000):
          print "1000th client --------------------------------------------->", RaffleList[999]
          RaffleWinner.append(RaffleList[499])
          # count = 5
        # else:
          # RaffleList.append(data_temp)
      result = "0"
      c.send("Done")

      while True:
        data = c.recv(1024)
        # print "FEP2 sending data to end server---",data
        if data:
          result = EndServer(data)
          # print result
          c.send(result)
        else:
          break
      
      cv.notify_all()
    
    else:
      cv.wait()
    
    cv.release()



# Client Thread Which adds request to Queue
def ClientThread(c):
  # print "CLIENT THREAD Started"
  cv.acquire() 
  ClientLoad.put(c)
  cv.notify_all()
  cv.release()

# This is our Work Dispenser which takes top 2 request and distributes it to out FEPs
def WorkDispatcher(num):
  i = 0
  while True:
    cv.acquire()
    if (ClientLoad.qsize() > 0):
      # print "Starting Work Dispatcher with Client Queue Size--",ClientLoad.qsize()
      i = i + 1
      if i == 1:
        # print "Sending request feom dispatcher to FEP1"
        FEP1Queue.put(ClientLoad.get())
        # ClientFEP1Queue.put(ClientQueue.get())
        cv.notify_all()
      if i == 2:
        # print "Sending request from dispatcher to FEP2"
        FEP2Queue.put(ClientLoad.get())
        # ClientFEP2Queue.put(ClientQueue.get())
        i = 0
        cv.notify_all()
    # cv.wait()
    else:
      cv.wait()
      
    cv.release()

# Global Variables

ThreadList = []

WorkQueue = Queue()  # THis Queue Stores all request from client. Top 2 request will be sent to FEP queues to process

FEP1Queue = Queue()  # This Queue stores request sent to FEP1 to handle

FEP2Queue = Queue()  # This queue stores requests sent to FEP2 to handle

ClientQueue = Queue()  # This Queue contains client info

ClientFEP1Queue = Queue()  # client info which are assigned to FEP1

ClientFEP2Queue = Queue()  # client info which are assigned to FEP2

ClientLoad = Queue()

RaffleList = []

RaffleWinner = []
#######



def Main():
    host = ""
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    # print("socket binded to post", port)
    s.listen(5)
    # print("socket is listening") 
    # a forever loop until client wants to exit
    ThreadNumber = 1
    while True:
        # establish connection with client
        c, addr = s.accept()
        # print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread for socket communication
        # print "Creating Client Threads Client",ThreadNumber
        # print " C " , c
        t = threading.Thread(target=ClientThread, args=(c,))
        ThreadList.append(t)
        t.start()
        ThreadNumber = ThreadNumber + 1
    # s.close()

if __name__ == '__main__':
  start_new_thread(WorkDispatcher, (1,))
  # start_new_thread(FEP1, (1,))
  # start_new_thread(FEP2, (1,))
  start_new_thread(startserver, (1,))
  start_new_thread(startserver1, (1,))
  start_new_thread(startserver2, (1,))
  start_new_thread(Winner, (1,))
  # start_new_thread(FEP1_socket, (1,))
  # start_new_thread(FEP2_socket, (1,))
  start_new_thread(FEP1, (1,))
  start_new_thread(FEP2, (1,))
  Main()

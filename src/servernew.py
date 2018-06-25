
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
from api import api
from restart.serving import Service
from random import *
#This function creates REST API server for each client which connects
service = Service(api)


def startserver(num):
    #print "RUNNIN SERVER REST--->"
    service.run(port=5000)
    return


def onConnectFEP1(conn,conn1):
  global busyFlagF1
  global fep1SocketClock
  print "----FEP1 CONNECTED WITH FEP2 SOCKET--->"
  #data = conn1.recv(1024)
  while 1:
    data = conn1.recv(1024)
    #print "DATA RCVD FROM FEP2--->",data
    if 'SYN_FEP2' in data:
      while 1:
        #cv.acquire()
        print "busyFlagF1-->",busyFlagF1
        if busyFlagF1 == 0:
          #print "busyFlagF1-->",busyFlagF1
          #print "SENDING ACK_FEP1 TO FEP2"
          conn1.send('ACK_FEP1')
          #cv.notify_all()
          break
        else:
          print "FEP1 waiting for busy flag"
          #cv.wait()
        #cv.release()
          #print "busyFlagF1-->",busyFlagF1
          #print conn.recv(1024)
  return

def onConnectFEP2(conn,conn1):
  global busyFlagF2
  global fep1SocketClock
  print "----FEP2 CONNECTED WITH FEP1 SOCKET-->",conn,conn1
  while 1:
    data = conn1.recv(1024)
    #print "DATA rcvd from FEP1--->",data
    if 'SYN_FEP1' in data:
      while 1:
        #cv.acquire()
        print "busyFlagF2-->",busyFlagF2
        if busyFlagF2 == 0:
          #print "busyFlagF2-->",busyFlagF2
          #print "SENDING ACK_FEP2 TO FEP1"
          conn1.send('ACK_FEP2')
          #cv.notify_all()
          break
        else:
          print "FEP1 waiting for busy flag"
          #cv.wait()
          #print "busyFlagF2-->",busyFlagF2
          #print conn.recv(1024)
        #cv.release()
      #if "SYN_FEP_SOCKET22" in data1:
        #print "MSG RCVD BY FEP2 SOCKET FROM FEP2---->",data1
  return



def FEP1_socket(num1):
  print "Starting FEP1 Socket"
  HOST = ''                 # Symbolic name meaning the local host
  PORT = 9092              # Arbitrary non-privileged port
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
  s.bind((HOST, PORT))
  s.listen(1)
  print "FEP1 SOCKET LISTNING ON PORT 9092"
  conn, addr = s.accept()
  print "Connected to FEP1 by",addr
  conn1,addr1 = s.accept()
  print 'Connected to FEP1 by', addr1
  #print conn.recv(1024)
  t = threading.Thread(target=onConnectFEP1, args=(conn,conn1,))
  t.start()
  #print conn.recv(1024)


  
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

def FEP2_socket(num1):
 print "Starting FEP2 Socket"
 HOST = ''                 # Symbolic name meaning the local host
 PORT = 9093              # Arbitrary non-privileged port
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 #s.setblocking(0)
 #fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
 s.bind((HOST, PORT))
 s.listen(1)
 print "FEP2 SOCKET LISTNING ON PORT 9093"
 conn, addr = s.accept()
 print 'Connected to FEP2 by', addr
 conn1,addr1 = s.accept() 
 print 'Connected to FEP2 by', addr1
 #print conn1.recv(1024)
 t = threading.Thread(target=onConnectFEP2, args=(conn,conn1,))
 t.start()


def Winner(num):
  print "Starting raffle winner"
  count = 0
  while True:
    cv.acquire()
    if len(RaffleWinner) == 10 and count == 0:
      x = randint(0,9)
      print "And the WINNER is--------->",RaffleWinner[x]
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
      print "100th client --------------------------------------------->",RaffleList[99]
      RaffleWinner.append(RaffleList[99])
      #count = 1
      cv.notify_all()
    elif (len(RaffleList) == 200 and count == 1):
      print "200th client --------------------------------------------->",RaffleList[199]
      RaffleWinner.append(RaffleList[199])
      #count = 2
      cv.notify_all()
    elif (len(RaffleList) == 300 and count == 2):
      print "300th client --------------------------------------------->",RaffleList[299]
      RaffleWinner.append(RaffleList[299])
      #count = 3
      cv.notify_all()
    elif (len(RaffleList) == 400 and count == 3):
      print "400th client --------------------------------------------->",RaffleList[399]
      RaffleWinner.append(RaffleList[399])
      #count = 4
      cv.notify_all()
    elif (len(RaffleList) == 500 and count == 4):
      print "500th client --------------------------------------------->",RaffleList[499]
      RaffleWinner.append(RaffleList[499])
      #count = 5
      cv.notify_all()
    else:
      cv.wait()
    cv.release()

def EndServer(data):
  #return data + " will be sent"
  data_temp = re.sub('[^A-Za-z0-9]+', '', data)
  if 'incrementMedalTally' in data_temp:
    url = "http://127.0.0.1:5000"+str(data)
    #print "Sending Reuest ",url
    data1 = requests.put(url).json()
  elif 'getMedalTally' in data_temp:
    url = "http://127.0.0.1:5000"+str(data)
    #print "Sending Request ",url
    data1 = requests.get(url).json()
  elif 'pushUpdate' in data_temp:
    url = "http://127.0.0.1:5000"+str(data)
    #print "Sending Request ",url
    data1 = requests.put(url)
  elif 'setScore' in data_temp:
    url = "http://127.0.0.1:5000"+str(data)
    #print "Sending request ",url
    data1 = requests.put(url).json()
    #print "Set Score",data1
  elif 'registerClient' in data_temp:
    url = "http://127.0.0.1:5000"+str(data)
    #print "Sending Request ",url
    data1 = requests.put(url)
  elif 'getScore' in data_temp:
    url = "http://127.0.0.1:5000"+str(data)
    #print "Sending Request ",url
    data1 = requests.get(url).json()
  return data1  

    
def FEP1(num):
  global busyFlagF1
  #global fep2Counter
  #global counter
  #global raf_dict
  print "Starting FEP1"
  start_new_thread(FEP1_socket, (1,))
  time.sleep(2)
  HOST = ''    # The remote host
  PORT = 9092              # The same port as used by the server
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))
  time.sleep(2)
  print "FEP2 connecting with FEP2 SOCKET"
  PORT = 9093
  s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s1.connect((HOST, PORT))
  while True:
    cv.acquire()
    if FEP1Queue.qsize() !=0:
      c = FEP1Queue.get()
      #print "FEP1 RECEIVING DATA"
      data = c.recv(1024)
      data_temp = re.sub('[^A-Za-z0-9]+', '', data)
      #print data_temp
      if 'Client' in data_temp:
        cname = data
        #print data_temp
        RaffleList.append(data_temp)
        
        if (len(RaffleList) == 100):
          print "100th client --------------------------------------------->",RaffleList[99]
          RaffleWinner.append(RaffleList[99])
          #count = 1
          #cv.notify_all()
        elif (len(RaffleList) == 200):
          print "200th client --------------------------------------------->",RaffleList[199]
          RaffleWinner.append(RaffleList[199])
          #count = 2
          #cv.notify_all()
        elif (len(RaffleList) == 300):
          print "300th client --------------------------------------------->",RaffleList[299]
          RaffleWinner.append(RaffleList[299])
          #count = 3
          #cv.notify_all()
        elif (len(RaffleList) == 400):
          print "400th client --------------------------------------------->",RaffleList[399]
          RaffleWinner.append(RaffleList[399])
          #count = 4
          #cv.notify_all()
        elif (len(RaffleList) == 500):
          print "500th client --------------------------------------------->",RaffleList[499]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        elif (len(RaffleList) == 600):
          print "600th client --------------------------------------------->",RaffleList[599]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        elif (len(RaffleList) == 700):
          print "700th client --------------------------------------------->",RaffleList[699]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        elif (len(RaffleList) == 800):
          print "800th client --------------------------------------------->",RaffleList[799]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        elif (len(RaffleList) == 900):
          print "900th client --------------------------------------------->",RaffleList[899]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        elif (len(RaffleList) == 1000):
          print "1000th client --------------------------------------------->",RaffleList[999]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        #else:
          #RaffleList.append(data_temp)

      result = "0"
      c.send("Done")
      
      while True:
        data = c.recv(1024)
        #print "FEP2 sending data to end server---",data
        if data:
          #fep1Counter += 0.0001
          #s.send('CLIENT')
          #d = s.recv(1024)
          #print "MSG RCVD FROM FEP@ SOCKET---->",d
          #print "SENDING SYN_FEP1 FROM FEP1"
          s1.send('SYN_FEP1')
          data1 = s1.recv(1024)
          #print "DATA RCVD FROM FEP2--->",data1
          if 'ACK_FEP2' in data1:
            #print "SENDING SYN_FEP1 FROM FEP1 TO FEP1"
            #s.send('SYN_FEP_SOCKET11')
            #print "PROCESSING"
            #s.send('REQUEST')
            busyFlagF1 = 1
            result = EndServer(data)
            #busyFlagF1 = 1
            #print result
            c.send(result)
            #if counter == 99:
              #print "_________________________100th______________   ",raf_dict[counter]
            #print "From FEP2---->",counter
            #raf_dict[counter] = cname 
            #counter += 1
            #raf_list.append(cname)
            if len(raf_list) == 100:
              print "_________________________100th______________   ",raf_list[99]
            raf_list.append(cname)
            busyFlagF1 = 0
        else:
          break
      
      cv.notify_all()
    
    else:
      cv.wait()
    
    cv.release()


def FEP2(num):
  global busyFlagF2 
  #global fep2Counter
  #global counter
  #global raf_dict
  print "Starting FEP2"
  start_new_thread(FEP2_socket,(1,))
  time.sleep(2)
  HOST = ''    # The remote host
  PORT = 9093              # The same port as used by the server
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))
  PORT = 9092
  time.sleep(2)
  s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print "FEP2 connecting with FEP1 SOCKET"
  s1.connect((HOST, PORT))
  while True:
    cv.acquire()
    if FEP2Queue.qsize() !=0:
      c = FEP2Queue.get()
      #ackMsg = "ACK"
      #f.send(ackMsg.encode('ascii'))
      #print "FEP2 RECEIVING DATA"
      data = c.recv(1024)
      data_temp = re.sub('[^A-Za-z0-9]+', '', data)
      if 'Client' in data_temp:
        cname = data
        #f.send(ackMsg.encode('ascii'))
        #f.send(data_temp.encode('ascii'))
        RaffleList.append(data_temp) 
        #print data_temp
        if (len(RaffleList) == 100):
          print "100th client --------------------------------------------->",RaffleList[99]
          RaffleWinner.append(RaffleList[99])
          #count = 1
          #cv.notify_all()
        elif (len(RaffleList) == 200):
          print "200th client --------------------------------------------->",RaffleList[199]
          RaffleWinner.append(RaffleList[199])
          #count = 2
          #cv.notify_all()
        elif (len(RaffleList) == 300):
          print "300th client --------------------------------------------->",RaffleList[299]
          RaffleWinner.append(RaffleList[299])
          #count = 3
          #cv.notify_all()
        elif (len(RaffleList) == 400):
          print "400th client --------------------------------------------->",RaffleList[399]
          RaffleWinner.append(RaffleList[399])
          #count = 4
          #cv.notify_all()
        elif (len(RaffleList) == 500):
          print "500th client --------------------------------------------->",RaffleList[499]
          RaffleWinner.append(RaffleList[499])
        elif (len(RaffleList) == 600):
          print "600th client --------------------------------------------->",RaffleList[599]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        elif (len(RaffleList) == 700):
          print "700th client --------------------------------------------->",RaffleList[699]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        elif (len(RaffleList) == 800):
          print "800th client --------------------------------------------->",RaffleList[799]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        elif (len(RaffleList) == 900):
          print "900th client --------------------------------------------->",RaffleList[899]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        elif (len(RaffleList) == 1000):
          print "1000th client --------------------------------------------->",RaffleList[999]
          RaffleWinner.append(RaffleList[499])
          #count = 5
        #else:
          #RaffleList.append(data_temp)
      result = "0"
      c.send("Done")

      while True:
        data = c.recv(1024)
        #print "FEP2 sending data to end server---",data
        if data:
          #fep2Counter += 0.0001
          #s.send('CLIENT')
          #d = s.recv(1024)
          #print "MSG RCVD FROM FEP@ SOCKET---->",d

          #print "SENDING SYN_FEP2 FROM FEP2"
          #sdata = "SYN_FEP2" + ":" + str(fep2Counter)
          s1.send('SYN_FEP2')
          data1 = s1.recv(1024)
          #print "DATA RCVD FROM FEP1--->",data1
          if 'ACK_FEP1' in data1:
            print "PROCESSING"
            #s.send('REQUEST')
            busyFlagF2 = 1
            result = EndServer(data)
            #print result
            c.send(result)
            #count += 1
            #if counter == 99:
              #print "_________________________100th______________   ",raf_dict[counter]
            #print counter
            #raf_dict[counter] = cname
            #counter += 1
            #raf_list.append(cname)
            if len(raf_list) == 100:
              print "_________________________100th_________________________________",raf_list[99]
            raf_list.append(cname)
            busyFlagF2 = 0
        else:
          break
      
      cv.notify_all()
    
    else:
      cv.wait()
    
    cv.release()



#Client Thread Which adds request to Queue
def ClientThread(c):
  #print "CLIENT THREAD Started"
  cv.acquire() 
  ClientLoad.put(c)
  cv.notify_all()
  cv.release()

#This is our Work Dispenser which takes top 2 request and distributes it to out FEPs
def WorkDispatcher(num):
  i = 0
  while True:
    cv.acquire()
    if (ClientLoad.qsize() > 0):
      #print "Starting Work Dispatcher with Client Queue Size--",ClientLoad.qsize()
      i = i + 1
      if i == 1:
        #print "Sending request feom dispatcher to FEP1"
        FEP1Queue.put(ClientLoad.get())
        #ClientFEP1Queue.put(ClientQueue.get())
        cv.notify_all()
      if i == 2:
        #print "Sending request from dispatcher to FEP2"
        FEP2Queue.put(ClientLoad.get())
        #ClientFEP2Queue.put(ClientQueue.get())
        i = 0
        cv.notify_all()
    #cv.wait()
    else:
      cv.wait()
      
    cv.release()

#Global Variables

ThreadList=[]

WorkQueue = Queue()   #THis Queue Stores all request from client. Top 2 request will be sent to FEP queues to process

FEP1Queue = Queue()   #This Queue stores request sent to FEP1 to handle

FEP2Queue = Queue()   #This queue stores requests sent to FEP2 to handle

ClientQueue = Queue() #This Queue contains client info

ClientFEP1Queue = Queue() #client info which are assigned to FEP1

ClientFEP2Queue = Queue() #client info which are assigned to FEP2

ClientLoad = Queue()

RaffleList = []

RaffleWinner = []


busyFlagF1 = 0

busyFlagF2 = 0

fep1Counter = 1.0000

fep2Counter = 2.0000

fep1SocketClock = 3.0000

fep2SocketClock = 4.0000

counter = 0


raf_dict = dict()

raf_list = []
#######



def Main():
    host = ""
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    #print("socket binded to post", port)
    s.listen(5)
    #print("socket is listening") 
    # a forever loop until client wants to exit
    ThreadNumber = 1
    while True:
        # establish connection with client
        c, addr = s.accept()
        #print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread for socket communication
        #print "Creating Client Threads Client",ThreadNumber
        #print " C " , c
        t = threading.Thread(target=ClientThread, args=(c,))
        ThreadList.append(t)
        t.start()
        ThreadNumber = ThreadNumber + 1
    #s.close()

if __name__ == '__main__':
  start_new_thread(WorkDispatcher, (1,))
  #start_new_thread(FEP1, (1,))
  #start_new_thread(FEP2, (1,))
  start_new_thread(startserver, (1,))
  start_new_thread(Winner, (1,))
  #start_new_thread(FEP1_socket, (1,))
  #start_new_thread(FEP2_socket, (1,))
  start_new_thread(FEP1, (1,))
  start_new_thread(FEP2, (1,))
  Main()

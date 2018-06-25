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
#from cache_tst import hash_dic
from xml.sax import default_parser_list
ThreadLock = threading.Lock()
cv = threading.Condition()
import re
import requests
from api import api as api_back
import hash
# from api2 import api as api_f2
# from api1 import api as api_f1
from restart.serving import Service
from random import *
import random
from api import var
import datetime
FEP1_timeDiff = 0
FEP2_timeDiff = 0

# print "API ID--->",bid
# This function creates REST API server for each client which connects
service = Service(api_back)
# service1 = Service(api_f1)
# service2 = Service(api_f2)
fep1TimeDiff = 0
fep2TimeDiff = 0

 #===============================================================================
 # IMPORTANT !!
 # FEP1 HAS A LOCAL CLOCK WHICH STARTS FROM 1.0000 AND INCREASE AS 1.0001, 
 # 1.0002,1.0003... 
 # SIMILARLY FEP2 HAS A LOCAL CLOCK WHICH STARTS AT 2.0000 AND FOLLOWS AS 2.0001,
 # 2.0002,...
 # ALOGORITM OF LOGICAL CLOCK SAYS THAT WHEN A MSG IS SENT FROM A SENDER IT
 # SENDS IT LOCAL CLOCK AND THE RECEIVER TICKS ITS CLOCK AND TAKE MAX OF WHAT
 # SENDER SENDS AND ITS OWN CLOCK.
 # FOR EXAMPLE SENDERLC(1.0003)--->RECEIVERLC(2.0004) 
 # -------> RECEIVERLC = MAX(1.0003,2.0004) + 0.0001
 #===============================================================================


def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()


#===============================================================================
# THIS MODULE IS RUNNING OUR REST API SERVICE
#===============================================================================


#===============================================================================
# URL_CONVERT
#===============================================================================
def url_convert(data):
    print "DATA--->",data
    if 'Rome' in data:
        data_str = '/getMedalTally/Rome'
    elif 'Gual' in data:
        data_str = '/getMedalTally/Gual'
    elif 'Stone Curling' in data:
        data_str = '/getScore/Stone Curling'
    elif 'Stone Throwing' in data:
        data_str = '/getScore/Stone Throwing'
    print "DAT_STR--->",data_str
    return data_str

#===============================================================================
# Ends here
#===============================================================================
def startserver(num):
    # print "RUNNIN SERVER REST--->"
    service.run(port=5000)
    
    return
# def startserver1(num):
#    # print "RUNNIN SERVER REST--->"
#    
#    service1.run(port=9090)
#    return

# def startserver2(num):
#    # print "RUNNIN SERVER REST--->"
#    
#    service2.run(port=9091)
#    return

#===============================================================================
# CODE ENDS HERE
#===============================================================================


#===============================================================================
# THIS IS MODULES RUN WHENEVER A SOMEONE TRIES TO CONNECT WITH FEP1. WE HAVE 2 
# ON FEP MODUEL IN OUR IMPLEMENTATIO.
#===============================================================================
def onConnectFEP1(conn1):

  global busyFlagF1
  global localCLKFEP1
  print "----FEP1 CONNECTED WITH FEP2 SOCKET--->", conn1
  # data = conn1.recv(1024)
  while 1:
    data = conn1.recv(1024)
    # print "DATA RCVD FROM FEP2--->",data
    if 'SYN_FEP2' in data:
      while 1:
        # cv.acquire()
        # print "busyFlagF1-->",busyFlagF1
        data_temp = data.split(':')
        float_temp_clock = float(data_temp[0])
        float_temp_clock = max(localCLKFEP1, float_temp_clock)
        float_temp_clock += 0.0001
        localCLKFEP1 = float_temp_clock
        print "FEP1 LOCAL CLOCK--------->", localCLKFEP1
        if busyFlagF1 == 0:
          # print "busyFlagF1-->",busyFlagF1
          # print "SENDING ACK_FEP1 TO FEP2"
          conn1.send('ACK_FEP1')
          # cv.notify_all()
          break
        else:
          print "FEP1 waiting for busy flag"
          # cv.wait()
        # cv.release()
          # print "busyFlagF1-->",busyFlagF1
          # print conn.recv(1024)
  return

#===============================================================================
# CODE ENDS HERE
#===============================================================================


#===============================================================================
# THIS IS MODULES RUN WHENEVER A SOMEONE TRIES TO CONNECT WITH FEP2. WE HAVE 2 
# ON FEP MODUEL IN OUR IMPLEMENTATIO.
#===============================================================================
def onConnectFEP2(conn1):
  global busyFlagF2
  global localCLKFEP2
  print "----FEP2 CONNECTED WITH FEP1 SOCKET-->", conn1
  while 1:
    data = conn1.recv(1024)
    # print "DATA rcvd from FEP1--->",data
    if 'SYN_FEP1' in data:
      while 1:
        # cv.acquire()
        # print "busyFlagF2-->",busyFlagF2
        data_temp = data.split(':')
        # print "CLOCK--------->",data_temp[0]
        if busyFlagF2 == 0:
          # print "busyFlagF2-->",busyFlagF2
          # print "SENDING ACK_FEP2 TO FEP1"
          data_temp = data.split(':')
          float_temp_clock = float(data_temp[0])
          float_temp_clock = max(localCLKFEP2, float_temp_clock)
          float_temp_clock += 0.0001
          localCLKFEP2 = float_temp_clock
          print "FEP2 LOCAL CLOCK--------->", localCLKFEP2
          conn1.send('ACK_FEP2')
          # cv.notify_all()
          break
        else:
          print "FEP1 waiting for busy flag"
          # cv.wait()
          # print "busyFlagF2-->",busyFlagF2
          # print conn.recv(1024)
        # cv.release()
      # if "SYN_FEP_SOCKET22" in data1:
        # print "MSG RCVD BY FEP2 SOCKET FROM FEP2---->",data1
  return

#===============================================================================
# CODE ENDS HERE
#===============================================================================

#===============================================================================
# THIS IS OUR SOCKET FOR FEP1 WHICH STARTES AS SOON AS FEP IS INITIATED.
#===============================================================================


def FEP1_socket(num1):
  print "--------Starting FEP1 Socket"
  HOST = ''  # Symbolic name meaning the local host
  PORT = 9092  # Arbitrary non-privileged port
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
  s.bind((HOST, PORT))
  s.listen(1)
  print "--------FEP1 SOCKET LISTNING ON PORT 9092"
  # conn, addr = s.accept()
  # print "Connected to FEP1 by", addr
  conn1, addr1 = s.accept()
  print 'Connected to FEP1 by', addr1
  # print conn.recv(1024)
  t = threading.Thread(target=onConnectFEP1, args=(conn1,))
  t.start()
  # print conn.recv(1024)
#===============================================================================
# CODE ENDS HERE
#===============================================================================


#===============================================================================
# THIS IS MODULES RUN WHENEVER A SOMEONE TRIES TO CONNECT WITH FEP. WE HAVE 2 
# ON FEP MODUEL IN OUR IMPLEMENTATION.
#===============================================================================
def FEP2_socket(num1):
 print "---------Starting FEP2 Socket"
 HOST = ''  # Symbolic name meaning the local host
 PORT = 9093  # Arbitrary non-privileged port
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 # s.setblocking(0)
 # fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
 s.bind((HOST, PORT))
 s.listen(1)
 print "------FEP2 SOCKET LISTNING ON PORT 9093"
 # conn, addr = s.accept()
 # print 'Connected to FEP2 by', addr
 conn1, addr1 = s.accept() 
 print 'Connected to FEP2 by', addr1
 # print conn1.recv(1024)
 t = threading.Thread(target=onConnectFEP2, args=(conn1,))
 t.start()

#===============================================================================
# CODE ENDS HERE
#===============================================================================

#===============================================================================
# THIS IS FEP1 CLOCK SERVER MODULE RUNS WHENEVER BERKELEY CLOCK SYNCHRONIZATION
# IS INITIATED 
#===============================================================================


def FEP1_Berk_socket(num1):
    try:
        print "Starting Berk FEP1 Socket"
        HOST = ''  # Symbolic name meaning the local host
        PORT = 9095  # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print "FEP1_BErk LSITNING"
        conn, addr = s.accept()
        print 'Leadr connected to FEP 1'
        data = conn.recv(1024)
        if data:
          if '1' not in data:
            print 'FEP 1 Not leader'
            print 'FEP 1 rcvd from Leader', data
            msg = time.time()
            conn.send(str(msg))
            # conn.send(msg.encode('ascii'))

            conn1, addr1 = s.accept()
            data = conn1.recv(1024)
            if data:
                print "LEADER SENT TIME DIFFEECNE TO FEP1", data
          else:
            print 'FEP1 RCVD Leader notification', data
            
            PORT = 9094
            s_new3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while 1:
              try:
                s_new3.connect((HOST, PORT))
                print 'AE:Leader FEP1 Connected with FEP2 Server'
                break
              except:
                continue
                print 'AE:Leader FEP1 cannot connect to FEP2'
            s_new3.send('FEP1')
            start_time = time.time()
            data = s_new3.recv(1024)
            if data:
                print 'Leader FEP1 rcvd time from backend', data
            t2_sent = float(data)
            t2_diff = time.time() - start_time
            t2 = t2_sent + t2_diff / 2
            ######Dummy send time diff######
            # print '^^^^^^^^^^^^^^^^Leader FEP1 sending time diff to FEP2^^^^^^^^^^^^^^^^^^^^^^^'
            # s_new4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s_new4.connect((HOST, PORT))
            # s_new4.send('Time diff')
            
            PORT = 5050
            s_new1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while 1:
              try:
                s_new1.connect((HOST, PORT))
                print 'AE:Leader FEP1 Connected with Backend Server'
                break
              except:
                continue
                print 'AE:Leader FEP1 cannot connect to Backend'
            s_new1.send('FEP1')
            start_time = time.time()
            data = s_new1.recv(1024)
            if data:
                print 'Leader Fep1 rcvd time from backend', data
            t3_sent = float(data)
            t3_diff = time.time() - start_time
            t3 = t3_sent + t3_diff / 2
            
            ######Dummy send time diff######
            # print '^^^^^^^^^^^^^^^^Leader Fep1 sending time diff to Backend^^^^^^^^^^^^^^^^^^^^^^^'
            # s_new2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s_new2.connect((HOST, PORT))
            # s_new2.send('Time diff')
            
            t1 = time.time()
            
            t = (t1 + t2 + t3) / 3

            global fep1TimeDiff

            fep1TimeDiff = t - t1

            PORT = 9094
            s_new4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_new4.connect((HOST, PORT))
            print 'Leader Fep1 sending time diff^'
            s_new4.send(str(t - t2))

            PORT = 5050
            s_new5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_new5.connect((HOST, PORT))
            print 'Leader Fep1 sending time diff'
            s_new5.send(str(t - t3))

        # FEP1_timeDiff = int(data)
        # print 'Connected by', addr
        
    except:
        print 'Error in FEP1 Berk Socket'

#===============================================================================
# FEP1 CLOCK SERVER ENDS HERE
#===============================================================================

#===============================================================================
# THIS IS FEP2 CLOCK SERVER MODULE RUNS WHENEVER BERKELEY CLOCK SYNCHRONIZATION
# IS INITIATED. THIS IS THE SERVER WHICH INITIATES THE LEADER ELECTION ELECTION.
#===============================================================================


def FEP2_Berk_socket(num1):
    try:
        print "Starting Berk FEP2 Socket"
        HOST = ''  # Symbolic name meaning the local host
        PORT = 9094  # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print "FEP2_BERK LSITNING"
        conn, addr = s.accept()
        data = conn.recv(1024)
        print 'Connected to FEP2 from Backend from addry', addr
          
        if data:
           print 'Vote received from Backend Servr', data

        # FEP2_timeDiff = int(data)
        # print 'Connected by', addr
        name = 'FEP2_Server'
        bid = random.randint(1, 10)
        vote = data + name + ':' + str(bid)
        print vote
        votes = vote.split(',')

        imax = 0
        leader = ''

        for vote in votes:

            temp = vote.split(':')
            val = int(temp[1])

            if val > imax:
                imax = val
                leader = temp[0]
        # print 'Leader', leader
        HOST = ''
        if leader.find('1') > 0:
            # url = "http://127.0.0.1:9090/votingResults/"+str(max)
            # requests.put(url)
            PORT = 9095
            print 'FEP 1 Leader'

        elif leader.find('2') > 0:
            # url = 'http://127.0.0.1:9091/votingResults/'+str(max)
            # data=requests.get(url).json()
            print 'FEP 2 Leader'

        else:
            # url = 'http://127.0.0.1:5000/votingResults/'+str(max)
            # data=requests.get(url).json()
            PORT = 5050
            print 'Backend Leader'
        # s.close()
        HOST = ''
        val = 1
        if val == 1:
          PORT = 5050
          s_new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          while 1:
            try:
              s_new.connect((HOST, PORT))
              print 'AE:Leader Connected with Backend Server'
              break
            except:
              print 'AE:Leader cannot connect to backend'
              continue
          s_new.send('FEP2')
          start_time = time.time()
          data = s_new.recv(1024)
          if data:
            print 'Time sent from backend', data
          t2_sent = float(data)
          t2_diff = time.time() - start_time
          t2 = t2_sent + t2_diff / 2
          s_new.close()
          print "NEW"       
        
          PORT = 9095
          s_new1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          while 1:
            try:
              s_new1.connect((HOST, PORT))
              print 'AE:Leader Connected with FEP1 Server'
              break
            except:
              continue
              print 'AE:Leader cannot connect to FEP1'
          s_new1.send('FEP2')
          start_time = time.time()
          data = s_new1.recv(1024)
          if data:
             print 'Time sent from FEP1', data
          t3_sent = float(data)
          t3_diff = time.time() - start_time
          t3 = t3_sent + t3_diff / 2
          s_new1.close()     
          
          t1 = time.time()

          t = (t1 + t2 + t3) / 3
          
          global fep2TimeDiff

          fep2TimeDiff = t - t1

          PORT = 5050
          s_new3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          while 1:
            try:
              s_new3.connect((HOST, PORT))
              print 'AE:Leader sends time difference Backend Server'
              break
            except:
              print 'AE:Leader cannot connect to backend'
              continue
          s_new3.send(str(t - t2))
          s_new3.close()
          # print "NEW"       
        
          PORT = 9095
          s_new4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          while 1:
            try:
              s_new4.connect((HOST, PORT))
              print 'AE:Leader sends tiem difference FEP1 Server'
              break
            except:
              continue
              print 'AE:Leader cannot connect to FEP1'
          s_new4.send(str(t - t3))
          # data=s_new1.recv(1024)
          # if data:
             # print '^^^^^^^^^Time sent from FEP1^^^^^^^^^^^',data
          s_new4.close() 

        elif val == 2:
          HOST = ''
          PORT = 5050
          s_new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          while 1:
            try:
              s_new.connect((HOST, PORT))
              print 'AE:FEP 2 declares Leader is Backend Server'
              break
            except:
              print 'AE:Fep 2 cannot connect to backend to declare leader'
              continue
          s_new.send('Backend')

          conn_4, addr_4 = s.accept()
          print 'Leadr connected to FEP 2'
          data = conn_4.recv(1024)
          if data:
            
            print 'FEP 2 Not leader'
            print 'FEP 2 rcvd from Leader', data
            msg = time.time()
            conn_4.send(str(msg))
            # conn_4.send(msg.encode('ascii'))

          conn_5, addr_5 = s.accept()
          data = conn_5.recv(1024)
          if data:
              print "LEADER SENT TIME DIFFEECNE TO FEP2", data

        else:
           HOST = ''
           PORT = 9095
           s_new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           while 1:
              try:
                s_new.connect((HOST, PORT))
                print 'AE:FEP 2 declares Leader is FEP1 Server'
                break
              except:
                print 'AE:Fep 2 cannot connect to fep1 to declare leader'
                continue
           s_new.send('FEP1')
           
           conn_4, addr_4 = s.accept()
           print 'Leadr connected to FEP 2'
           data = conn_4.recv(1024)
           if data:
            
              print 'FEP 2 Not leader'
              print 'FEP 2 rcvd from Leader', data
              msg = time.time()
              conn_4.send(str(msg))
              # conn_4.send(msg.encode('ascii'))

           conn_5, addr_5 = s.accept()
           data = conn_5.recv(1024)
           if data:
                print "*************LEADER SENT TIME DIFFEECNE TO FEP2***********", data
           
    except:
        print 'Error in FEP2 Berk SocketS'

#===============================================================================
# FEP2 CLOCK SERVER ENDS HERE
#===============================================================================

#===============================================================================
# THIS IS THE MODULE WHICH INITIATES THE VOTING FIRST TIME BY INTIATING TIME
# SERVERS FOR BOTH FEP(TEMP SOCKETS NOT ACTUAL FEP SERVERS )
# WE HAVE USED DIFFERENT SOCKETS FOR MAIN FEP1 AND FEP2 SERVERS) 
#===============================================================================

    
def castVoteFEP1(num):
    # time.sleep(10)
    print "STARTING CAST VOTE"
    start_new_thread(FEP1_Berk_socket, (1,))
    start_new_thread(FEP2_Berk_socket, (1,))
    
    name = 'Fep_1_Server'
    bid = random.randint(1, 10)
    vote = name + ':' + str(bid) + ','
    # print "BID_____________________",var
    
    # url = "http://127.0.0.1:9091/castVote/" + str(vote)
    # print "Sending Reuest ",url
    # requests.put(url)
    # time.sleep(10)
    
    HOST = ''
    PORT = 5050
    print "********CONNECTING CASTVOTE TO BACKEND****************"
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
      try:
        s1.connect((HOST, PORT))
        print 'Connected with Backend Server'
        break
      except:
        continue
    s1.send(vote)

#===============================================================================
# CODE ENDS HERE
#===============================================================================


#===============================================================================
# THIS THREAD IS MONITORING RAFFLE_WINNER LIST . IT RANDOMLY PICKS A WINNER AMONGST
# THE CLIENTS WHO WERE ENTERED INTO THE CONTEST.THESE CIENTS WERE 
# 100TH , 200TH ...1000TH CLIENT.
#===============================================================================
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

#===============================================================================
# CODE ENDS HERE
#===============================================================================


#===============================================================================
# THIS THREAD IS JUST MONITORING raf_LIST WHICH IS THE LIST WHICH CONTAINS THE 
# CLIENTS REQUEST.
#===============================================================================
def RaffleLottery(num):
  print "-----Starting Raffle Lottery-------"
  count = 0
  while True:
    # cv.acquire()
    # print len(raf_list)
    if (len(raf_list) == 100 and count == 0):
      print "100th client --------------------------------------------->", raf_list[99]
      RaffleWinner.append(raf_list[99])
      count = 1
      # cv.notify_all()
    elif (len(raf_list) == 200 and count == 1):
      print "200th client --------------------------------------------->", raf_list[199]
      RaffleWinner.append(raf_list[199])
      count = 2
      # cv.notify_all()
    elif (len(raf_list) == 300 and count == 2):
      print "300th client --------------------------------------------->", raf_list[299]
      RaffleWinner.append(raf_list[299])
      count = 3
      # cv.notify_all()
    elif (len(raf_list) == 400 and count == 3):
      print "400th client --------------------------------------------->", raf_list[399]
      RaffleWinner.append(raf_list[399])
      count = 4
      # cv.notify_all()
    elif (len(raf_list) == 500 and count == 4):
      print "500th client --------------------------------------------->", raf_list[499]
      RaffleWinner.append(raf_list[499])
      count = 5
      # cv.notify_all()
    elif (len(raf_list) == 600 and count == 5):
      print "600th client --------------------------------------------->", raf_list[599]
      RaffleWinner.append(raf_list[599])
      count = 6
      # cv.notify_all()

    elif (len(raf_list) == 700 and count == 6):
      print "700th client --------------------------------------------->", raf_list[699]
      RaffleWinner.append(raf_list[699])
      count = 7
      # cv.notify_all()

    elif (len(raf_list) == 800 and count == 7):
      print "800th client --------------------------------------------->", raf_list[499]
      RaffleWinner.append(raf_list[799])
      count = 8
      # cv.notify_all()

    elif (len(raf_list) == 900 and count == 8):
      print "900th client --------------------------------------------->", raf_list[499]
      RaffleWinner.append(raf_list[899])
      count = 9
      # cv.notify_all()

    elif (len(raf_list) == 1000 and count == 9):
      print "1000th client --------------------------------------------->", raf_list[499]
      RaffleWinner.append(raf_list[999])
      count = 10
      # cv.notify_all()
    # else:
      # cv.wait()
    # cv.release()
    
#===============================================================================
# CODE ENDS HERE
#===============================================================================

#===============================================================================
# THIS THREAD TAKES REQUEST FROM FEPS AND FORWARD THEM TO OUR BACKEND SERVER.
# THE FINAL RESULT IS RETURNED FROM HERE TO FEP.
#===============================================================================


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

#===============================================================================
# CODE ENDS HERE
#===============================================================================


#===============================================================================
# THIS IS ONE OF OUR REPLICATED SERVER CALLED FEP1. THIS FEP IS LISTNING TO THE 
# DISPATCHER TO INSERT LOAD IN ITS QUEUE.
#===============================================================================
def FEP1(num):
  global busyFlagF1
  # global fep2Counter
  # global counter
  # global raf_dict
  global localCLKFEP1
  print "Starting FEP1"
  start_new_thread(FEP1_socket, (1,))
  r_list = []
  time.sleep(2)
  HOST = ''  # The remote host
  PORT = 9092  # The same port as used by the server
  # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # s.connect((HOST, PORT))
  time.sleep(2)
  print "FEP2 connecting with FEP2 SOCKET"
  PORT = 9093
  s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s1.connect((HOST, PORT))
  while True:
    cv.acquire()
    if FEP1Queue.qsize() != 0:
      c = FEP1Queue.get()
      # print "FEP1 RECEIVING DATA"
      data = c.recv(1024)
      data_temp = re.sub('[^A-Za-z0-9]+', '', data)
      # print data_temp
      if 'Client' in data_temp:
        cname = data
      elif 'Cacofonix' in data_temp:
        cname = 'NULL'
      result = "0"
      c.send("Done")
      while True:
        data = c.recv(1024)
        if data:
          localCLKFEP1 += 0.0001
          tmp = str(localCLKFEP1) + ':' + 'SYN_FEP1'
          print "FEP1 sending data to FEP2--->", tmp
          s1.send(tmp)
          data1 = s1.recv(1024)
          # print "DATA RCVD FROM FEP2--->",data1
          if 'ACK_FEP2' in data1:
            busyFlagF1 = 1
            data_hash = hash.encode(data)
            if data_hash in cache_dic.keys():
                result_1 = []
                result_1 = cache_dic[data_hash]
                if result_1[1] == 0:
                    print "F1:****CACHE HIT******"
                    result = result_1[0]
                    print "FF1:********FROM LOCAL CACHE--->",result
                else:
                    result = EndServer(data)
                    print "F1:************Removing DIRTY RESULT FROM CACHE**********"
                    del cache_dic[data_hash]
            else:
                if 'incrementMedalTally' in data or 'setScore' in data:
                    print "f1:data recvd---->",data
                    result = EndServer(data)
                    url_con = url_convert(data)
                    data_hash_temp = hash.encode(url_con)
                    if data_hash_temp in cache_dic.keys():
                        temp_list = []
                        temp_list = list(cache_dic[data_hash_temp])
                        temp_list[1] = 1
                        cache_dic[data_hash_temp] = temp_list
                        print "F1:****ADDING 1 TO DIRTY BIT******",cache_dic[data_hash_temp]
                else:
                    result = EndServer(data)
                    print "F1*******CACHE MISS***********"
                    if len(cache_dic) < 5:
                        r_list = []
                        r_list.append(result)
                        r_list.append(0)
                        cache_dic[data_hash] = r_list
                        print "F1:***********ADDING ELEMENT INTO CACHE*********",cache_dic[data_hash]

                    else:
                        print "F1:*******REMOVING FIRST ELEMENT FROM CACHE*********"
                        for k in cache_dic:
                            del cache_dic[k]
                            break
                        r_list = []
                        r_list.append(result)
                        r_list.append(0)
                        cache_dic[data_hash] = r_list
                        print "F1:****ADDING NEW ELEMENT IN CACHE******",cache_dic[data_hash]
            try:
                print 'Current Berk Sync Time'
                print  time.time() + FEP1_timeDiff
            except:
                print 'Berkeley Clock Error or unavailable'
            a1 = datetime.datetime.now().time()
            b = addSecs(a1, fep1TimeDiff)
            result1 = 'Last Updated on ' + str(b) + ' ' + str(result)
            c.send(result1)           
            if 'Client' in cname:
              raf_list.append(cname)
            busyFlagF1 = 0
        else:
          break
      
      cv.notify_all()
    
    else:
      cv.wait()
    
    cv.release()

#===============================================================================
# CODE ENDS HERE
#===============================================================================

#===============================================================================
# THIS IS ONE OF OUR REPLICATED SERVER CALLED FEP2. THIS FEP IS LISTNING TO THE 
# DISPATCHER TO INSERT LOAD IN ITS QUEUE.
#===============================================================================


def FEP2(num):
  global busyFlagF2 
  r_list = []
  # global fep2Counter
  # global counter
  # global raf_dict
  global localCLKFEP2
  print "Starting FEP2"
  start_new_thread(FEP2_socket, (1,))
  time.sleep(2)
  HOST = ''  # The remote host
  PORT = 9093  # The same port as used by the server
  # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # s.connect((HOST, PORT))
  HOST = '' 
  PORT = 9092
  time.sleep(2)
  s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print "FEP2 connecting with FEP1 SOCKET"
  s1.connect((HOST, PORT))
  # while 1:
    # try:
      # s1.connect((HOST, PORT))
      # print ('CONNECTED TO PORT 9092 FROM FEP2')
      # break
    # except:
      # continue
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
        cname = data
      elif 'Cacofonix' in data_temp:
        cname = 'NULL'
      result = "0"
      c.send("Done")

      while True:
        data = c.recv(1024)
        if data:
          localCLKFEP2 += 0.0001
          tmp = str(localCLKFEP2) + ':' + 'SYN_FEP2'
          print "FEP2 sending data to fep1----->", tmp
          s1.send(tmp)
          data1 = s1.recv(1024)
          # print "DATA RCVD FROM FEP1--->",data1
          if 'ACK_FEP1' in data1:
            # print "PROCESSING"
            # s.send('REQUEST')
            busyFlagF2 = 1
            data_hash = hash.encode(data)
            if data_hash in cache_dicf2.keys():
                result_1 = []
                result_1 = cache_dicf2[data_hash]
                if result_1[1] == 0:
                    print "F2:****CACHE HIT******"
                    result = result_1[0]
                    print "F2:********FROM LOCAL CACHE--->",result
                else:
                    result = EndServer(data)
                    print "F1:************Removing DIRTY RESULT FROM CACHE**********"
                    del cache_dicf2[data_hash]
            else:
                if 'incrementMedalTally' in data or 'setScore' in data:
                    print "f2:data recvd---->",data
                    result = EndServer(data)
                    url_con = url_convert(data)
                    data_hash_temp = hash.encode(url_con)
                    if data_hash_temp in cache_dicf2.keys():
                        temp_list = []
                        temp_list = list(cache_dicf2[data_hash_temp])
                        temp_list[1] = 1
                        cache_dicf2[data_hash_temp] = temp_list
                        print "F2:****ADDING 1 TO DIRTY BIT******",cache_dicf2[data_hash_temp],result
                else:
                    result = EndServer(data)
                    print "F2*******CACHE MISS***********"
                    if len(cache_dicf2) < 5:
                        r_list = []
                        r_list.append(result)
                        r_list.append(0)
                        cache_dicf2[data_hash] = r_list
                        print "F2:***********ADDING ELEMENT INTO CACHE*********",cache_dicf2[data_hash]

                    else:
                        print "F2:*******REMOVING FIRST ELEMENT FROM CACHE*********"
                        for k in cache_dic:
                            del cache_dicf2[k]
                            break
                        r_list = []
                        r_list.append(result)
                        r_list.append(0)
                        cache_dicf2[data_hash] = r_list
                        print "F2:****ADDING NEW ELEMENT IN CACHE******",cache_dicf2[data_hash]
            #result = EndServer(data)
            try:
                print 'Current Berk Sync Time'
                print  time.time() + FEP2_timeDiff
            except:
                print 'Berkeley Clock Error or unavailable'            
            a1 = datetime.datetime.now().time()
            b = addSecs(a1, fep2TimeDiff)
            result1 = 'Last Updated on ' + str(b) + ' ' + str(result)
            c.send(result1)           
            if 'Client' in cname:
              raf_list.append(cname)
            busyFlagF2 = 0
        else:
          break
      
      cv.notify_all()
    
    else:
      cv.wait()
    
    cv.release()

#===============================================================================
# END OF CODE
#===============================================================================


#===============================================================================
# THIS THREAD IS CALLED FOR EACH CLIENT WHICH CONNECTS TO OUR SERVER.IT TAKES A 
# CLIENT AND LOAD THE CLIENT ONTO CLIENT LOAD QUEUE.
#===============================================================================
# Client Thread Which adds request to Queue
def ClientThread(c):
  # print "CLIENT THREAD Started"
  cv.acquire() 
  ClientLoad.put(c)
  cv.notify_all()
  cv.release()

#===============================================================================
# CODE ENDS HERE
#===============================================================================

#===============================================================================
# THIS IS OUR WORK DISPENSER , WHOSE MAIN TASK IS TO SEND REQUEST TO EITHER FEP1 
# OR FEP2.THIS IS SENDING THE CLIENT NOT ITS REQUEST.WE HAVE DESIGNED THIS SUCH 
# THAT THE FIRST REQUEST FROM ANY CLIENT GOES TO FEP1 AND SECOND GOES TO FEP2.
#===============================================================================


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

#===============================================================================
# CODE ENDS HERE
#===============================================================================

#===============================================================================
# THE FOLLOWING VARIABLES ARE GLOBAL VARIABLES.
# FEP1Queue: CONTAINS CLIENT INFO WHICH IS BEEN GIVEN TO FEP1 TO PROCESS ITS REQUEST
# FEP1Queue: CONTAINS CLIENT INFO WHICH IS BEEN GIVEN TO  FEP2 TO PROCESS ITS REQUEST
# ClientQueu: CONTAINS INFO ABOUT THE CLIENT
# RAF_LIST: CONTAINS ORDERED LIST OF CLIENTS STARTING FROM 0 TO N.
# RAFFLEWINNER: STORES 1OOTH , 200TH ... 1000TH CLIENT INFO.
#===============================================================================


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

busyFlagF1 = 0

busyFlagF2 = 0

localCLKFEP1 = 1.0000

localCLKFEP2 = 2.0000

counter = 0

raf_dict = dict()

raf_list = []

cache_dic = {}

cache_dicf2 = {}
#######

#===============================================================================
# CODE ENDS HERE
#===============================================================================

#===============================================================================
# THIS IS OUR MAIN CODE WHICH OPENS THE SOCKET, ALLOW SNCHRONIZATION
#===============================================================================


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
#===============================================================================
# CODE ENDS HERE
#===============================================================================

#===============================================================================
# ALL THE THREAD WHICH WILL START
#===============================================================================


if __name__ == '__main__':
  start_new_thread(WorkDispatcher, (1,))
  start_new_thread(startserver, (1,))
  # castVoteFEP1()
  start_new_thread(castVoteFEP1, (1,))
 # start_new_thread(startserver2, (1,))
  start_new_thread(Winner, (1,))
  start_new_thread(RaffleLottery, (1,))
  start_new_thread(FEP1, (1,))
  start_new_thread(FEP2, (1,))
  Main()
  
#=============================================================================
# PROGRAM ENDS HERE 
#=============================================================================
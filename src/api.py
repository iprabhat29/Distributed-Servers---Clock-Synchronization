#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================

from restart.api import RESTArt
from restart.utils import load_resources
import threading
import socket
from thread import *
import time
import random

# def startRestAPI():
#
vote = ''
id = 0
name = 'BackEnd'


#---new
var = 0

api = RESTArt()

# Load all resources
load_resources(['resource'])
load_resources(['resource1'])
load_resources(['resource2'])
load_resources(['resource3'])
load_resources(['resource4'])
load_resources(['resource5'])
load_resources(['resource6'])
load_resources(['resource7'])


def Backend_socket(num1):
    global var
    bid =random.randint(1,10)
    name='Backend'
    vote=name+':'+str(bid)+','
    print "Starting Backend_socket on 5050"
    try:
        HOST = ''  # Symbolic name meaning the local host
        PORT = 5050  # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print "----------BACKEND LSITNING-----------"
        conn, addr = s.accept()
        print '----------------------Connected to Backend from addry----------------------', addr
        data = conn.recv(1024)
        if data:
          
           #print '^^^^^^Backend is not Leader^^^^^^^^'
           print '----------Vote received from FEP1-------',data
           HOST=''
           PORT = 9094
           s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           while 1:
             try:
               fvote=data+vote
               s1.connect((HOST, PORT))
              
               print '-------------Backend Connected with FEP 2 Server-------------------'
               break
             except:
               continue
           s1.send(fvote)
            #s.listen(1)
        
        conn1,addr1=s.accept()
        print '^^^^^^^^^^^^^^^^^Backend Connected to Leader^^^^^^^^^^^^^^^^^^^^^'
        data = conn1.recv(1024)
        if '1'in data or '2' in data:
            print '^^^^^^^^^^Backened not the leader^^^^^^^^^^^^^',data
            msg=time.time()
            conn1.send(str(msg))
            #conn1.send(msg.encode('ascii'))
            print '^^^^^^^^^^Backened sent time to leader^^^^^^^^^^^^^'
            #global timeDiff
            #timeDiff = int(data)

            conn2,add2 = s.accept()

            data = conn2.recv(1024)

            if data:
                print "*************LEADER SENT TIME DIFFEECNE TO BACKEDN***********",data
                #---new
                var = data
        else:
            print '^^^^^^^^^^^^^^^^^^^^^Backend is the Leader^^^^^^^^^^^^^^^^^^^^^^',data
            
            PORT=9095
            s_new1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while 1:
              try:
                s_new1.connect((HOST, PORT))
                print '^^^^^^^^^^^^AE:Leader Backend Connected with FEP1 Server^^^^^^^^^^^^^^^^^'
                break
              except:
                continue
                print '^^^^^^^^^^^^AE:Leader Backend cannot connect to FEP1^^^^^^^^^^^^^^^^^^^^^'
            s_new1.send('Backend')
            start_time=time.time()
            data=s_new1.recv(1024)
            if data:
                print '^^^^^^^^^^^^^^^^^^^^Leader Backend rcvd time from backend^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',data
            t2_sent=float(data)
            t2_diff=time.time()-start_time
            t2=t2_sent+t2_diff/2

            ######Dummy send time diff######
            #print '^^^^^^^^^^^^^^^^Leader Backend sending time diff to FEP1^^^^^^^^^^^^^^^^^^^^^^^'
            #s_new2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s_new2.connect((HOST, PORT))
            #s_new2.send('Time diff')


            PORT=9094
            s_new3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while 1:
              try:
                s_new3.connect((HOST, PORT))
                print '^^^^^^^^^^^^AE:Leader Backend Connected with FEP2 Server^^^^^^^^^^^^^^^^^'
                break
              except:
                continue
                print '^^^^^^^^^^^^AE:Leader Backend cannot connect to FEP2^^^^^^^^^^^^^^^^^^^^^'
            s_new3.send('Backend')
            start_time=time.time()
            data=s_new3.recv(1024)
            if data:
                print '^^^^^^^^^^^^^^^^^^^^Leader Backend rcvd time from backend^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',data
            t3_sent=float(data)
            t3_diff=time.time()-start_time
            t3=t3_sent+t3_diff/2
            ######Dummy send time diff######
            #print '^^^^^^^^^^^^^^^^Leader Backend sending time diff to FEP2^^^^^^^^^^^^^^^^^^^^^^^'
            #s_new4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s_new4.connect((HOST, PORT))
            #s_new4.send('Time diff')

            t1=time.time()

            t=(t1+t2+t3)/3
            #--new
            var = t

            PORT=9094
            s_new4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_new4.connect((HOST, PORT))
            s_new4.send(str(t-t3))

            PORT=9095
            s_new5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_new5.connect((HOST, PORT))
            s_new5.send(str(t-t2))

    except:
        print 'Unable to connect Backend Socket listener'

start_new_thread(Backend_socket, (1,))

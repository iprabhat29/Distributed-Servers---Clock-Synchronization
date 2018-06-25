#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================
# Import socket module
import socket
import time 
import threading
from thread import *

import time



# Starting Main segment of the code


#===============================================================================
# Client1 Prabhat is a Roman and is interested only in score of Rome from time 
# to time. The request sent will be "/getMedalTally/Rome".Prabhat sends a request 
# upn receiving result  closes its stonetab.  
#===============================================================================
def Client1(num):
  while True:
    # print "Starting Client1"
    # local host IP '127.0.0.1'
    start_time = time.time()
    host = '127.0.0.1'
    # Define the port on which you want to connect
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    a = s.connect((host, port))
    if a == 0:
      print "Connected"
    message = "Client1"
    message1 = "/getMedalTally/Rome"  # This client is interested in medal tally of Rome since he is "ROME"
    a = 0
    # print "Sending Request from Client1-->",message
    s.send(message.encode('ascii'))
    data = s.recv(1024)
    # time.sleep(10)
    print "Sending Request from Client1-->", message1
    s.send(message1.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED from FEP by client1--->", data
      #data = s.recv(1024)
      #if data:
        #print "TIMESTAMP--------------------",data
      print 'Time taken for processing request', time.time() - start_time
      # time.sleep(1)
        # return
    s.close()
    
#===============================================================================
# CODE ENDS HERE
#===============================================================================


#===============================================================================
# Client1 APOORVA is a GUALAN and is interested only in score of Rome from time 
# to time. The request sent will be "/getMedalTally/gual".Apoorva sends a request 
# upn receiving result  closes its stonetab.  
#===============================================================================

def Client2(num):
  while True:
    # print "Starting Client2"
    # local host IP '127.0.0.1'
    start_time = time.time()
    host = '127.0.0.1'
    # Define the port on which you want to connect
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    a = s.connect((host, port))
    if a == 0:
      print "Connected"
    # message you send to server
    message = "Client2"
    message1 = "/getMedalTally/Gual"  # This client is interested in medal tally of Rome since he is "Gualan"
    a = 0
    # print "Sending Request from Client2-->",message
    s.send(message.encode('ascii'))
    data = s.recv(1024)
    print "Sending Request from Client2-->", message1
    s.send(message1.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED by client2 from FEP--->", data
      print 'Time taken for processing request', time.time() - start_time
      # time.sleep(1)
    s.close()
#===============================================================================
# Client3, MR. BUSH is a Roman and is interested only in score of Rome from time 
# to time. The request sent will be "/getMedalTally/Rome".MR. BUSH sends a request 
# upOn receiving result  closes its stonetab.  
#===============================================================================

def Client3(num):
  while True:
    # print "Starting Client3"
    # local host IP '127.0.0.1'
    start_time = time.time()
    host = '127.0.0.1'
    # Define the port on which you want to connect
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    a = s.connect((host, port))
    if a == 0:
      print "Connected"
    # message you send to server
    message = "Client3"
    message1 = "/getMedalTally/Rome"  # This client is interested in medal tally of Rome since he is "Gualan"
    a = 0
    # print "Sending Request from Client3-->",message
    s.send(message.encode('ascii'))
    data = s.recv(1024)
    print "Sending Request from Client3-->", message1
    s.send(message1.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED by Client3 from FEP--->", data
      print 'Time taken for processing request', time.time() - start_time
      # time.sleep(1)
    s.close()

#===============================================================================
# CODE ENDS HERE
#===============================================================================


#===============================================================================
# Client4 , MR. MODI is a Roman and is interested only in score of Rome from time 
# to time. The request sent will be "/getMedalTally/Rome".MR. MODI sends a request 
# upn receiving result  closes its stonetab.  
#===============================================================================
def Client4(num):
  while True:
    # print "Starting Client4"
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    start_time = time.time()
    # Define the port on which you want to connect
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    a = s.connect((host, port))
    if a == 0:
      print "Connected"
    # message you send to server
    message = "Client4"
    message1 = "/getMedalTally/Rome"  # This client is interested in medal tally of Rome since he is "Gualan"
    a = 0
    # print "Sending Request from Client2-->",message
    s.send(message.encode('ascii'))
    data = s.recv(1024)
    print "Sending Request from Client4-->", message1
    s.send(message1.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED by client4 from FEP--->", data
      print 'Time taken for processing request', time.time() - start_time
      # time.sleep(1)
    s.close()

#===============================================================================
# CODE ENDS HERE
#===============================================================================



#===============================================================================
# CLIENT 5 , MR. CLINTON IS A ROMAN WHO JUST WANTS TO KNOW THE LATEST SCORE OF 
# BOTH ROME AND GUAL IN STONE CURLING.HE IS A BIG STONE CURLING FAN.HE IS NEUTRAL.
#===============================================================================

def Client5(num):
  while True:
    # print "Starting Client5"
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    start_time = time.time()
    # Define the port on which you want to connect
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    a = s.connect((host, port))
    if a == 0:
      print "Connected"
    # message you send to server
    message = "Client5"
    message1 = message1 = "/getScore/Stone Throwing"  # This client is interested in medal tally of Rome since he is "Gualan"
    a = 0
    # print "Sending Request from Client5-->",message
    s.send(message.encode('ascii'))
    data = s.recv(1024)
    print "Sending Request from Client5-->", message1
    s.send(message1.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED by client5 from FEP--->", data
      print 'Time taken for processing request', time.time() - start_time
      # time.sleep(1)
    s.close()
#===============================================================================
# CODE ENDS HERE
#===============================================================================




#===============================================================================
# CLIENT 6 , MR. LINCOLN IS A ROMAN WHO JUST WANTS TO KNOW THE LATEST SCORE OF 
# BOTH ROME AND GUAL IN STONE CURLING.HE IS A BIG STONE CURLING FAN.HE IS NEUTRAL.
#===============================================================================

def Client6(num):
  while True:
    
    # print "Starting Client4"
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    start_time = time.time()
    # Define the port on which you want to connect
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    a = s.connect((host, port))
    if a == 0:
      print "Connected"
    # message you send to server
    message = "Client6"
    message1 = "/getScore/Stone Curling"  # This client is interested in medal tally of Rome since he is "Gualan"
    a = 0
    # print "Sending Request from Client6-->",message
    s.send(message.encode('ascii'))
    data = s.recv(1024)
    print "Sending Request from Client6-->", message1
    s.send(message1.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED by client6 from FEP--->", data
      print 'Time taken for processing request', time.time() - start_time
      # time.sleep(1)
    s.close()

#===============================================================================
# CODE ENDS HERE
#===============================================================================




#===============================================================================
# CACOFONIX IS OUR THE ONE WHO UPDATES THE SCORE , WE HAVE TAKE FEW EXAMPLES ON
# UPDATE 
# 1. FIRST MSG IS TO UPDATE STONE THROWING SCORE OF ROME(300) GUAL(600).THESE 
# NUMBERS CAN BE RANDOMLY CHOOSEN.BUT WE HAVE MADE IT FIXED.CAN BE SCALED LATER 
# TO RANDOM.
# 2. SECOND MSG IS TO ICREMENT SILVER MEDAL TALLY OF ROME BY ONE SINCE IN STONE
# CURLING EVENT IT HAS LOST TO GUAL.
# 3. THIRD MESSAGE IS TO UPDATE THE MEDAL TALLY OF GUAL BY 1 SINCE IT WONE 
# STONE THROWING EVENT.
# 4. FOURTH MESSAGE IS SAME AS 1 INSTEAD OF STONE THROWING ITS SENDING 
# SCORES FOR STONE CURLING.
#===============================================================================

def Cacofonix(num):
  while True:
    
    # print "Starting Cacofonix"
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    # Define the port on which you want to connect
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    a = s.connect((host, port))
    if a == 0:
      print "Connected"
    
    # message you send to server
    message = "Cacofonix"


    # print "Sending Request from Cacofonix-->",message
    s.send(message.encode('ascii'))
    data = s.recv(1024)

    message1 = "/setScore/Stone Throwing/300/600/Cacofonix"

    message2 = "/incrementMedalTally/Rome/Silver/Cacofonix"

    message3 = "/incrementMedalTally/Gual/Gold/Cacofonix"

    message4 = "/setScore/Stone Curling/300/600/Cacofonix"

    print "Sending Request from Cacofonix-->", message1
    s.send(message1.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED by Cacofonix from FEP--->", data
      # time.sleep(1)
    

    print "Sending Request from Cacofonix-->", message2
    s.send(message2.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED by Cacofonix from FEP--->", data
      # time.sleep(1)

    
    print "Sending Request from Cacofonix-->", message3
    s.send(message3.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED by Cacofonix from FEP--->", data
      # time.sleep(1)


    print "Sending Request from Cacofonix-->", message4
    s.send(message4.encode('ascii'))
    data = s.recv(1024)
    if data:
      print "DATA RECEIVED by Cacofonix from FEP--->", data
      # time.sleep(1)

    s.close()    
#===============================================================================
# MODULE ENDS HERE 
#===============================================================================




#===============================================================================
# THIS MAIN FUNCTION STARTS THREADONE BY ONE STARTING FROM CLIENT1,CLIENT2,...,CLIENT6
# AND CACOFONIX IN ORDER.
#===============================================================================
def Main():
  print "Starting Main"
  # start_new_thread(Client1, (1,))
  t1 = threading.Thread(target=Client1, args=(1,))
  t2 = threading.Thread(target=Client2, args=(1,))
  t3 = threading.Thread(target=Client3, args=(1,))
  t4 = threading.Thread(target=Client4, args=(1,))
  t5 = threading.Thread(target=Client5, args=(1,))
  t6 = threading.Thread(target=Client6, args=(1,))
  t7 = threading.Thread(target=Cacofonix, args=(1,))
  t1.start()
  t2.start()
  t3.start()
  t4.start()
  t5.start()
  t6.start()
  t7.start()
#===============================================================================
# CODE ENDS HERE
#===============================================================================



if __name__ == '__main__':
  # start_new_thread(Client1, (1,))                                #starting rest for this client, this is different for server REST.Starting with Port 5051 and localhost.
  Main()
  # start_new_thread(Client2, (1,))


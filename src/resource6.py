#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================

from restart.resource import Resource

from api import api
import json

import time
import random
import requests
import socket


@api.register(pk='<int:id>')
class votingResults(Resource):
    name = 'votingResults'

    def index(self, request):
        return ''

    def read(self, request, id):
        t1=time.time()
        
        start_time = time.time()
        url1 = 'http://127.0.0.1:9090/getTime'
        t2_sent=requests.get(url1,timeout=10)
        t2_diff=(time.time() - start_time)
        t2=t2_sent+t2_diff/2
        
        start_time = time.time()
        url2 = 'http://127.0.0.1:9091/getTime'
        t3_sent=requests.get(url2,timeout=10)
        t3_diff=(time.time() - start_time)
        t3=t3_sent+t3_diff
        
        t=(t1+t2+t3)/3
        
        print 'Time difference of Backend Server',t-t1
        print 'Time difference of Fep 1 Server',t-t2
        print 'Time difference of Fep 2 Server',t-t3
        
        
        host = ""
        port = 9095
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        msg=str(t-t2).encode('ascii')
        s.send(msg)
        host = ""
        port = 9094
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        msg=str(t-t3).encode('ascii')
        s.send(msg)
        
        return 'Success'

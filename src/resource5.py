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

@api.register(pk='<string:vote>')
class castVote(Resource):
    name = 'castVote'
    def index(self, request):
        return ''

    def replace(self, request, vote):
        name = 'BackEnd_Server'
        id = random.randint(1, 10)
        vote = vote + name + ':' + str(id) 
        print vote
        votes = vote.split(',')

        max=0
        leader=''
        url=''

        for vote in votes:
            
            temp = vote.split(':')
            val=int(temp[1])
        
            if val > max:
                max = val
                leader=temp[0]
        print 'Leader', leader
        if leader.find('1')>0:
            url = "http://127.0.0.1:9090/votingResults/"+str(max)
            #requests.put(url)
            
            
        elif leader.find('2')>0:
            url = 'http://127.0.0.1:9091/votingResults/'+str(max)
            #data=requests.get(url).json()
            
        else:
            url = 'http://127.0.0.1:5000/votingResults/'+str(max)
            #data=requests.get(url).json()
        print url
        #time.sleep(10)
        #url='http://127.0.0.1:5000/getMedalTally'
        requests.get(url)
		
        return 'Success'

		


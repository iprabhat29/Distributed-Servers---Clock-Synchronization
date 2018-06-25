#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================
from __future__ import absolute_import

from restart.resource import Resource

from api2 import api
import json
import requests
import time
import random

@api.register(pk='<string:vote>')
class castVote(Resource):
    name = 'castVote'
    def index(self, request):
        return ''

    def replace(self, request, vote):
        name = 'Fep_2_Server'
        id = random.randint(1, 10)
        vote = vote + name + ':' + str(id) + ','
        url = 'http://127.0.0.1:5000/castVote/' + str(vote)
        requests.put(url,timeout=10)
        print vote
        return 'Success'


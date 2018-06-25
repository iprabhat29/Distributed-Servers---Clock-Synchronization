#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================
from restart.resource import Resource

from api import api
import json

import time


@api.register()
class getTime(Resource):
    name = 'getTime'

    def index(self, request):
        data=time.time()
        
        return data
        
    def read(self, request):
        print 'Here'
        data=time.time()
        
        return data

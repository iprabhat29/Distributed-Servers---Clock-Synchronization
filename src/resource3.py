#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================
from __future__ import absolute_import

from restart.resource import Resource

from api import api
import BackEnd
import json
import time

@api.register(pk='<string:clientID>/<string:eventType>/<string:port>')
class registerClient(Resource):
    name = 'registerClient'

    def index(self, request):
        return []
    
    def replace(self, request, clientID, eventType, port):
        data=BackEnd.getDataJSON();
        print 'Current Berk Sync Time'
        print time.time() + BackEnd.getTimeDiff()
        data['Clients'].append({'clientID':clientID,'port':port})
      
        if eventType == "Stone Curling":
            BackEnd.updateDataJSON(data)
        else:
            print "NOT ADDED"
        return "Success"

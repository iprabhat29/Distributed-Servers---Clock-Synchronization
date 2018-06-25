
#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================

from restart.resource import Resource

from api import api
import json
import BackEnd
import time


@api.register(pk='<string:eventType>')
class getScore(Resource):
    name = 'getScore'

    def index(self, request):
        return []
        
    def read(self, request, eventType):
        print 'Current Berk Sync Time'
        print time.time() + BackEnd.getTimeDiff()
        data=BackEnd.getDataJSON();
        dat1 = data['Team']['Gual'][eventType]['Score']
        dat2 = data['Team']['Rome'][eventType]['Score']
        ret=json.dumps({'Gual':dat1,'Rome':dat2})
        
        return ret

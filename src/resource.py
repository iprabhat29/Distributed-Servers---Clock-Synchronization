#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================

from restart.resource import Resource
import BackEnd
from api import api
#from jsonify import convert
import json
import time


@api.register(pk='<string:teamName>')
class getMedalTally(Resource):
    name = 'getMedalTally'

    def index(self, request):
        print 'Current Berk Sync Time'
        print time.time() + BackEnd.getTimeDiff()
        data=BackEnd.getDataJSON();
        dat1 = data['Team']['Gual']
        dat2 = data['Team']['Rome']
        dat1.pop('Stone Skating',0)
        dat1.pop('Stone Curling',0)
        dat1.pop('Stone Throwing',0)
        dat2.pop('Stone Skating',0)
        dat2.pop('Stone Curling',0)
        dat2.pop('Stone Throwing',0)
        ret={'Gual':dat1,'Rome':dat2}
        return json.dumps(ret)
    
    def read(self, request, teamName):
        print 'Current Berk Sync Time'
        print time.time() + BackEnd.getTimeDiff()
        data=BackEnd.getDataJSON();
        for e in data['Team']:
            if e == teamName:
                dat = data['Team'][e]
        dat.pop('Stone Curling',0)
        dat.pop('Stone Throwing',0)
        dat.pop('Stone Skating',0)
        return json.dumps({teamName:dat})

#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================
from restart.resource import Resource

from api import api
import requests
import BackEnd
import json
import time


@api.register(pk='<string:eventType>/<string:rome_score>/<string:gaul_score>/<string:auth_id>')
class setScore(Resource):
    name = 'setScore'

    def index(self, request):
        return []

    def replace(self, request, eventType, rome_score, gaul_score,auth_id ):
        print 'Current Berk Sync Time'
        print time.time() + BackEnd.getTimeDiff()
        if auth_id == 'Cacofonix':
            data=BackEnd.getDataJSON();
            for e in data['Team']:
                if e == 'Rome':
                    data['Team'][e][eventType]['Score'] = rome_score
                if e == 'Gual':
                    data['Team'][e][eventType]['Score'] = gaul_score
            BackEnd.updateDataJSON(data)
  
            data=BackEnd.getDataJSON();
            dat1 = data['Team']['Gual'][eventType]['Score']
            dat2 = data['Team']['Rome'][eventType]['Score']
#             if eventType == "Stone Curling":
#                 a = data['Clients']
#                 flag = set()     # creating a set to ignore duplicate port so that notification is passed over to correct clients
#                 for i in a:
#                     flag.add(str(i['port']))
#                     for i in flag:
#                         print i
#                     url = "http://127.0.0.1:"+i+"/pushUpdate/Stone Curling/"+rome_score+"/"+gaul_score
#                     requests.put(url)
            return json.dumps({'Gual':dat1,'Rome':dat2})

        else:
            return "Failure to add Authorization failed"


#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================

from restart.resource import Resource

from api import api
import BackEnd
import json
import time


@api.register(pk='<string:teamName>/<string:medalType>/<string:auth_id>')
class incrementMedalTally(Resource):
    name = 'incrementMedalTally'

    def index(self, request):
        return []
        
    def replace(self, request, teamName,medalType,auth_id):
        print 'Current Berk Sync Time'
        print time.time() + BackEnd.getTimeDiff()
        if auth_id == 'Cacofonix':
            data=BackEnd.getDataJSON();
            for e in data['Team']:
                if e == teamName:
                    if medalType == 'Gold':
                        data['Team'][teamName]['Gold'] +=1 
                    if medalType == 'Silver':
                        data['Team'][teamName]['Silver'] += 1
                    if medalType == 'Bronze':
                        data['Team'][teamName]['Bronze'] += 1

            BackEnd.updateDataJSON(data)
            return json.dumps({teamName:data['Team'][teamName]})
        else:
            return 'Not Authorized'


#===============================================================================
# # Contributors:
#    Prabhat Bhatt 
#    Apoorva Saxena
#===============================================================================

from restart.api import RESTArt
from restart.utils import load_resources
import threading
import socket
from thread import *
import time

# def startRestAPI():
#
vote = ''
id = 0
name = 'Fep_1_Server'

api = RESTArt()

# Load all resources
load_resources(['resource_fep1'])
load_resources(['resource1_fep1'])
load_resources(['resource2_fep1'])




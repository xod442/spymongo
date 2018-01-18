
'''
 Copyright 2016 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__copyright__ = "Copyright 2017, wookieware."
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

Script reads state change messages from OneView and builds local mongo database
collections

1. Vlan database
2. Network-set database
3  Internetconnect Group database
----------------------------------------------------------------------------------------------------
'''
import pika, ssl
from optparse import OptionParser
from pika.credentials import ExternalCredentials
import json
import logging
import pymongo
from pymongo import MongoClient

host = '10.1.9.175'

logging.basicConfig()


ssl_options = ({"ca_certs": "caroot.pem",
               "certfile": "client.pem",
               "keyfile": "key.pem",
               "cert_reqs": ssl.CERT_REQUIRED,
               "server_side": False})

# Connect to RabbitMQ


print ("Connecting")
connection = pika.BlockingConnection(
               pika.ConnectionParameters(
                       host, 5671, credentials=ExternalCredentials(),
                       ssl=True, ssl_options=ssl_options))
# Get all, etheret-networks and write to the vlan collection
# Create and bind to queue

# Get all, etheret-networks and write to the vlan collection
#ethernet_nets = connection.ethernet_networks.get_all()
print connection.channel


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

Script reads state change messages from OneView and builds local mongo databases

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


logging.basicConfig()

# Create client connector

client = MongoClient('db:mongo', 27017)
# client = MongoClient('172.20.0.2:27017')
# client = MongoClient('localhost',27017)

# Define database
db = client.pov2

# define the collections
vlans = db.vlan
netsets = db.netset
ligs = db.lig

# Callback function that handles messages

def callback(ch, method, properties, body):
    record = body.decode('utf-8')
    msg = json.loads(record)
    resource = msg['resource']

    # Write vlan updates

    if resource['category'] == 'ethernet-networks':
      vlans.insert(resource)
      print 'Record inserted: vlans'

    # Wirte network sets update

    if resource['category'] == 'network-sets':
      netsets.insert(resource)
      print 'Record inserted: netsets'

    # Write logical interconnect group update

    if resource['category'] == 'logical-interconnect-groups':
      ligs.insert(resource)
      print 'Record inserted: ligs'





'''
Pem Files needed, be sure to replace the \n returned from the APIs with CR/LF
caroot.pem - the CA Root certificate   - GET /rest/certificates/ca
client.pem, first POST /rest/certificates/client/rabbitmq Request body: {"type":"RabbitMqClientCert","commonName":"default"}

GET /rest/certificates/client/rabbitmq/keypair/default
client.pem is the key with  -----BEGIN CERTIFICATE-----
key.pem is the key with -----BEGIN RSA PRIVATE KEY-----
Setup our ssl options
'''

ssl_options = ({"ca_certs": "caroot.pem",
               "certfile": "client.pem",
               "keyfile": "key.pem",
               "cert_reqs": ssl.CERT_REQUIRED,
               "server_side": False})

parser = OptionParser()
parser.add_option('--host', dest='host',
        help='Pika server to connect to (default: %default)',
        default='10.1.9.175',
)

options, args = parser.parse_args()

# Connect to RabbitMQ

host = options.host
print ("Connecting to %s:5671, to change use --host hostName " %(host))
connection = pika.BlockingConnection(
               pika.ConnectionParameters(
                       host, 5671, credentials=ExternalCredentials(),
                       ssl=True, ssl_options=ssl_options))

# Create and bind to queue

EXCHANGE_NAME = "scmb"
ROUTING_KEY = "scmb.#"

channel = connection.channel()
result = channel.queue_declare()
queue_name = result.method.queue

channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=ROUTING_KEY)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

# Start listening for messages

channel.start_consuming()

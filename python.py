import pika, ssl
from optparse import OptionParser
from pika.credentials import ExternalCredentials
import json
import logging

logging.basicConfig()

###############################################
# Callback function that handles messages
def callback(ch, method, properties, body):
    msg = json.loads(body)
    timestamp = msg['timestamp']
    resourceUri = msg['resourceUri']
    resource = msg['resource']
    changeType = msg['changeType']

    print
    #print (body)
    #print ("%s: Message received:" %(timestamp))
    #print ("Routing Key: %s" %(method.routing_key))
    print ("Change Type: %s" %(changeType))
    #print ("Resource URI: %s" %(resourceUri))
    #print ("Resource: %s" %(resource))

#   Pem Files needed, be sure to replace the \n returned from the APIs with CR/LF
#   caroot.pem - the CA Root certificate   - GET /rest/certificates/ca
#   client.pem, first POST /rest/certificates/client/rabbitmq Request body: {"type":"RabbitMqClientCert","commonName":"default"}
#   GET /rest/certificates/client/rabbitmq/keypair/default
#   client.pem is the key with  -----BEGIN CERTIFICATE-----
#   key.pem is the key with -----BEGIN RSA PRIVATE KEY-----
# Setup our ssl options
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

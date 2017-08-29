# Running the application

                  _     _                _                                      _            _                                    _     _            
  /\/\  _   _ ___| |_  | |__   ___    __| | ___  _ __   ___    ___  _ __     __| | ___   ___| | _____ _ __   _ __ ___   __ _  ___| |__ (_)_ __   ___ 
 /    \| | | / __| __| | '_ \ / _ \  / _` |/ _ \| '_ \ / _ \  / _ \| '_ \   / _` |/ _ \ / __| |/ / _ \ '__| | '_ ` _ \ / _` |/ __| '_ \| | '_ \ / _ \
/ /\/\ \ |_| \__ \ |_  | |_) |  __/ | (_| | (_) | | | |  __/ | (_) | | | | | (_| | (_) | (__|   <  __/ |    | | | | | | (_| | (__| | | | | | | |  __/
\/    \/\__,_|___/\__| |_.__/ \___|  \__,_|\___/|_| |_|\___|  \___/|_| |_|  \__,_|\___/ \___|_|\_\___|_|    |_| |_| |_|\__,_|\___|_| |_|_|_| |_|\___|

- Checkout code on https://github.com/xod442/spymongo.git save it on the /opt directory on your docker machine.

-In order for spymongo.py to register and listen on the SCMB a couple
of things need to happen first.

#1. The HPE OneView appliance needs to generate a Rabbit MQ keypair. This does
not happen by default and must be done ONE TIME for the running HPE OneView
appliance. 

#2. The script needs to download a copy of the SSL key and certificate to the /opt directory.....Do it! 

For Example: assuming, you have a brand new HPE OneView appliance invocation
would be similar to this:

# Generate the RabbitMQ keypair on the appliance

  ./scmb.py -a [HPE OneView Appliance IP] -u Administrator -p MyPass -g

# Download the SSL key and certificate

  ./scmb.py -a [HPE OneView Appliance IP] -u Administrator -p MyPass -d

Once those two commands have run one time:

# Issue the following docker commands

- Build the containers: `docker-compose build`  (This will build the reader application container)
- Start mongodb separately: `docker-compose up -d db` (This will start the mongo database)
- Start the app: `docker-compose up reader` ( This is start the reader application container)


# To access mongodb
- Find the docker web container name and run: `docker exec -it (reader container) mongo`
  docker exec -it (reader app)  mongo --host mongodb

# To run tests
- Find the docker web container name and run: `docker exec -it (reader container) python tests.py`


# Gets into the shell of the app container
docker exec -it (reader container) bash



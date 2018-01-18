# Running the application
MUST BE RUN IN A DOCKER CONTAINER


                  _     _                _                                      _            _                                    _     _
  /\/\  _   _ ___| |_  | |__   ___    __| | ___  _ __   ___    ___  _ __     __| | ___   ___| | _____ _ __   _ __ ___   __ _  ___| |__ (_)_ __   ___
 /    \| | | / __| __| | '_ \ / _ \  / _` |/ _ \| '_ \ / _ \  / _ \| '_ \   / _` |/ _ \ / __| |/ / _ \ '__| | '_ ` _ \ / _` |/ __| '_ \| | '_ \ / _ \
/ /\/\ \ |_| \__ \ |_  | |_) |  __/ | (_| | (_) | | | |  __/ | (_) | | | | | (_| | (_) | (__|   <  __/ |    | | | | | | (_| | (__| | | | | | | |  __/
\/    \/\__,_|___/\__| |_.__/ \___|  \__,_|\___/|_| |_|\___|  \___/|_| |_|  \__,_|\___/ \___|_|\_\___|_|    |_| |_| |_|\__,_|\___|_| |_|_|_| |_|\___|

- Checkout code on https://github.com/xod442/spymongo.git save it on the /opt directory on your docker machine.

       - cd /opt
       - git clone https://github.com/xod442/spymongo.git
       - cd spymongo

-In order for spymongo.py to register and listen on the SCMB a couple of things need to happen first.

#1. The HPE OneView appliance needs to generate a Rabbit MQ keypair.
This does not happen by default and must be done ONE TIME for the running HPE OneView
appliance.

#2. The script needs to download a copy of the SSL key and certificate (pem files) to the /opt directory.....Do it!

NOTE!!!!!The .pem files in the repository and they are mine. They will not work. Remove them or overwrite them.

For Example: assuming, you have a brand new HPE OneView appliance invocation ould be similar to this:

# Generate the RabbitMQ keypair on the appliance

  ./scmb.py -a [HPE OneView Appliance IP] -u Administrator -p MyPass -g    # My pass is for oneView

# Download the SSL key and certificate

  ./scmb.py -a [HPE OneView Appliance IP] -u Administrator -p MyPass -d    # MyPass is for oneView

Once those two commands have run one time:

# Issue the following docker command(s) (still working on the docker-compose file)

---------------------------------------------------------------------------------------------------------
- Build the container(s): `docker-compose build`  (This will build the reader application container)
- Start mongodb separately: `docker run --name spy-db -d mongo` (This will start the mongo database)
- Start/Link the app: `docker run --name spymongo --link spy-db:mongo -d spymongo_reader python spymongo.py <IP of oneView>`

( This will take a sec...please wait... starting the reader application container)


# To access mongodb
- Run: `docker exec -it spy-db bash`

  Once at the container shell type: mongo
  You will be inside the mongo database

  Mongo commands:
  show dbs
  use<db_name>
  show collections
  db.<collection-name>.count()  print number of records
  db.<collection-name>.find()   prints table


# Gets into the shell of the app container
docker exec -it spymongo_reader bash

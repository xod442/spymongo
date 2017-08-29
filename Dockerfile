#
# scmb reader
#
#

# Pull base image.
FROM python:3.4.5-slim

# Get some custom packages
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    gcc \
    python3-dev \
    mongodb

## make a local directory
RUN mkdir /opt/scmb

# set the working directory from which CMD, RUN, ADD references
WORKDIR /opt/scmb

# now copy all the files in this directory to /code
ADD . .

# pip install the local requirements.txt
RUN pip3 install -r requirements.txt

# start the app server
CMD python ./spymongo.py 10.1.9.175

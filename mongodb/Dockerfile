#
# MongoDB Dockerfile
#
# https://github.com/dockerfile/mongodb
#

# Pull base image.
FROM dockerfile/ubuntu

# Install MongoDB.
RUN \
  apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 && \
  echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' > /etc/apt/sources.list.d/mongodb.list && \
  apt-get update && \
  apt-get install -y mongodb-org && \
  rm -rf /var/lib/apt/lists/*

# Define mountable directories.
VOLUME ["/data/db"]

# Define working directory.
WORKDIR /data

# Define default command.
#CMD ["mongod"]
CMD ["mongod --httpinterface"]
# Expose ports.
#   - 27017: process
#   - 28017: http
EXPOSE 27017
EXPOSE 28017


RUN for f in openvre/install/database/*.json; do mongoimport --host myServer --db mongodb -u myAdmin -p myPassword --authenticationDatabase admin $f; done



#FROM alpine:3.9
# alpine 3.9 has mongodb 4.0.5-r0 in community repository
# https://pkgs.alpinelinux.org/packages?name=mongodb&branch=v3.9
#RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/main' >> /etc/apk/repositories \
#    && echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories \
#    && apk update \
#    && apk add mongodb
#CMD ["/bin/sleep","1d"]
~                       

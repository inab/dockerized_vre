# Dockerfile
#FROM php:7.4-cli
#FROM php:7-apache
#FROM ubuntu:latest
FROM php:7.2.7-fpm

#RUN apk update && \
#    apk upgrade && \
#    apk add git
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y && apt-get install -y git\
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libpng-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) gd

RUN git clone https://github.com/inab/openvre.git
RUN cd openvre
RUN pwd
RUN mkdir openvre/data
RUN mkdir openvre/data/shared_data
RUN cp -r openvre/install/data/* openvre/data/shared_data/
RUN pwd

RUN cd openvre/public

#RUN cp openvre/config/globals.inc.php.sample openvre/config/globals.inc.php

RUN mkdir -p /home/user/openvre/logs/
RUN touch /home/user/openvre/logs/application.log
RUN chown -R www-data:www-data  /home/user/openvre/logs/application.log

#RUN cp openvre/config/mail.conf.sample openvre/config/mail.conf 
#RUN cp openvre/config/mongo.conf.sample openvre/config/mongo.conf 
#RUN cp openvre/config/oauth2.conf.sample openvre/config/oauth2.conf 
#RUN cp openvre/config/oauth2_admin.conf.sample openvre/config/oauth2_admin.conf 

#add cleaning step adjusting the document + sistema de cues
#chmod u+x scripts/maintainance/cleanUsersData.php
#crontab -e

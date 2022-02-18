# Dockerfile
#FROM php:7.4-cli
#FROM php:7-apache
#FROM ubuntu:latest
FROM php:7.3-fpm

#RUN apk update && \
#    apk upgrade && \
#    apk add git
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y autoconf pkg-config libssl-dev
RUN pecl install mongodb
RUN docker-php-ext-install bcmath
RUN echo "extension=mongodb.so" >> /usr/local/etc/php/conf.d/mongodb.ini

# Install Laravel dependencies
RUN apt-get install -y \
        git libfreetype6-dev \
        libjpeg62-turbo-dev \
        libmcrypt-dev \
        libpng-dev

RUN apt-get update && apt-get install -y libmcrypt-dev \ 
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install gd


#RUN apt-get update && apt-get install -y && apt-get install -y git \
#        libfreetype6-dev \
#        libjpeg62-turbo-dev \
#        libpng-dev \
#    && docker-php-ext-configure gd --with-freetype --with-jpeg \
#    && docker-php-ext-install -j$(nproc) gd

#RUN apt-get update && apt-get install -y zlib1g-dev libicu-dev g++ libssl-dev

# Install mongo
#RUN pecl install mongodb \
#&& echo "extension=mongodb.so" > /usr/local/etc/php/conf.d/ext-mongodb.ini

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /var/www/html
#RUN git clone https://github.com/inab/openVRE.git
RUN git clone https://github.com/Socayna/openVRE.git
RUN touch caca
RUN cd openVRE
WORKDIR /var/www/html/openVRE
RUN composer update
#RUN service apache2 restart
RUN mkdir logs
RUN touch logs/application.log
RUN chown -R www-data:www-data  logs/application.log
RUN pwd
RUN mkdir -p /data/shared_data
RUN cp -r install/data/* /data/shared_data/
RUN pwd
RUN cd public

#RUN cp openvre/config/globals.inc.php.sample openvre/config/globals.inc.php
#RUN cp openvre/config/mail.conf.sample openvre/config/mail.conf 
#RUN cp openvre/config/mongo.conf.sample openvre/config/mongo.conf 
#RUN cp openvre/config/oauth2.conf.sample openvre/config/oauth2.conf 
#RUN cp openvre/config/oauth2_admin.conf.sample openvre/config/oauth2_admin.conf 

#add cleaning step adjusting the document + sistema de cues
#chmod u+x scripts/maintainance/cleanUsersData.php
#crontab -e

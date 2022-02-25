# Dockerfile
#FROM php:7.4-cli

FROM webdevops/php-apache:7.4

#COPY ./demo.apache.conf /usr/local/apache2/conf/apache.conf

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y autoconf pkg-config libssl-dev
#RUN pecl install mongodb
RUN docker-php-ext-install bcmath
RUN echo "extension=mongodb.so" >> /usr/local/etc/php/conf.d/mongodb.ini

RUN apt-get install -y \
        git libfreetype6-dev \
        libjpeg62-turbo-dev \
        libmcrypt-dev \
        libpng-dev

RUN apt-get update && apt-get install -y libmcrypt-dev \ 
    && docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
    && docker-php-ext-install gd 

#COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer

WORKDIR /var/www/html
RUN git clone https://github.com/inab/openVRE.git
#RUN git clone https://github.com/Socayna/openVRE.git
RUN pwd
RUN cd openVRE
WORKDIR /var/www/html/openVRE
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN composer self-update
RUN composer update --ignore-platform-req=ext-mongodb --ignore-platform-req=ext-mongodb
RUN mkdir logs
RUN touch logs/application.log
RUN chown -R www-data:www-data  logs/application.log
RUN pwd
RUN cp logs/application.log /var/www/html/openVRE/config

#VOLUME ["/shared_data"]
#RUN mkdir /shared_data
RUN pwd
RUN mkdir -p /shared_data/public
RUN cp -r -v install/data/* /shared_data/
RUN chown -R  www-data:www-data /shared_data/

RUN pwd
RUN cd public


ENV WEB_DOCUMENT_ROOT=/var/www/html/openVRE/public/
WORKDIR /var/www/html/openVRE/public
RUN pwd
EXPOSE 88 443

ENTRYPOINT ["/opt/docker/bin/entrypoint.sh"]

CMD ["supervisord"]


#RUN cp openvre/config/globals.inc.php.sample openvre/config/globals.inc.php
#RUN cp openvre/config/mail.conf.sample openvre/config/mail.conf 
#RUN cp openvre/config/mongo.conf.sample openvre/config/mongo.conf 
#RUN cp openvre/config/oauth2.conf.sample openvre/config/oauth2.conf 
#RUN cp openvre/config/oauth2_admin.conf.sample openvre/config/oauth2_admin.conf 

#add cleaning step adjusting the document + sistema de cues
#chmod u+x scripts/maintainance/cleanUsersData.php
#crontab -e

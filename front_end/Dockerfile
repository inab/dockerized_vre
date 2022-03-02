# Dockerfile
FROM webdevops/php-apache:7.4

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y autoconf pkg-config libssl-dev
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

RUN apt-get update && apt-get install -y gnupg software-properties-common
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN add-apt-repository 'deb https://repo.mongodb.org/apt/debian buster/mongodb-org/4.2 main'
RUN apt-get update
RUN apt-get install -y mongodb-org

RUN mongo --version
RUN mongoimport --version

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
RUN mkdir /shared_data
RUN pwd
RUN cp -r -v install/data/* /shared_data/
RUN chown -R  www-data:www-data /shared_data/
RUN pwd
RUN cd public

#RUN for f in install/database/*.json; do mongoimport --host my-mongodb --db open-vre -u ${MONGO_ADMIN} -p ${MONGO_ADMIN_PASS} --authenticationDatabase admin $f; done
#RUN for f in install/database/*.json; do mongoimport --host my-mongodb --db open-vre --collection vre-collection $f; done


ENV WEB_DOCUMENT_ROOT=/var/www/html/openVRE/public/
WORKDIR /var/www/html/openVRE/public
RUN pwd
EXPOSE 88 443

ENTRYPOINT ["/opt/docker/bin/entrypoint.sh"]

CMD ["supervisord"]


#CMD ["for f in install/database/*.json; do mongoimport --host my-mongodb  --db open-vre --collection vre-collection -u admin -p admin --authenticationDatabase admin $f; done"]

#add cleaning step adjusting the document + sistema de cues
#chmod u+x scripts/maintainance/cleanUsersData.php
#crontab -e

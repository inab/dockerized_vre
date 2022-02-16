FROM webdevops/apache:ubuntu-16.04

#ENV WEB_PHP_SOCKET=$PHP_SOCKET

COPY ./demo.apache.conf /usr/local/apache2/conf/apache.conf
RUN pwd

ENV WEB_DOCUMENT_ROOT=/var/www/html/openvre/public/

WORKDIR /var/www/html/openvre/public
RUN pwd 
RUN ls
#EXPOSE 88 443

ENTRYPOINT ["/opt/docker/bin/entrypoint.sh"]

CMD ["supervisord"]

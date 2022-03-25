FROM ubuntu:14.04.4
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq ; apt-get upgrade ; \
    apt-get install -y gridengine-master gridengine-exec gridengine-client; \
    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# dummy user account
RUN useradd -m dummy
RUN echo "dummy:dummy" | chpasswd
#

ADD setup_gridengine.sh /usr/local/bin/setup_gridengine.sh
RUN chmod +x /usr/local/bin/setup_gridengine.sh

#CMD /usr/local/bin/setup_gridengine.sh && echo sgeclient >> /etc/hosts && qconf -as mail.domain.es 

CMD /usr/local/bin/setup_gridengine.sh && tail -f /var/spool/gridengine/qmaster/messages && echo "hostname ; date" | qsub && qconf -as sgeclient.shared


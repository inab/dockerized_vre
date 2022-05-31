FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y && apt-get install -y gnupg2 vim
RUN echo 'deb http://ftp.debian.org/debian/ stretch main contrib non-free\n\
deb http://security.debian.org/debian-security/ stretch/updates main contrib non-free\n' > /etc/apt/sources.list.d/debian.list

RUN echo 'Package: gridengine-*\n\
Pin: release o=Debian\n\
Pin-Priority: 1000\n\
\n\
Package: *\n\
Pin: release o=Debian\n\
Pin-Priority: 10\n' > /etc/apt/preferences.d/debian

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys AA8E81B4331F7F50
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 112695A0E562B32A
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 04EE7237B7D453EC
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EF0F382A1A7B6500
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 648ACFD622F3D138
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0E98404D386FA1D9

RUN apt-get -y update
RUN apt-get install debian-archive-keyring
RUN apt-key add /usr/share/keyrings/debian-archive-keyring.gpg
RUN apt-get install -y gridengine-exec gridengine-master gridengine-qmon
#RUN mkdir /var/lib/gridengine/qmon
RUN ln -s /usr/share/gridengine/pixmaps /var/lib/gridengine/qmon/PIXMAPS

RUN apt-get update -y && apt install -y docker.io

#RUN apt-get update -qq ; apt-get upgrade ; \
#    apt-get install -y gridengine-master gridengine-exec gridengine-client; \
#    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# dummy user account
RUN useradd -m dummy
RUN echo "dummy:dummy" | chpasswd
#

ADD setup_gridengine.sh /usr/local/bin/setup_gridengine.sh
RUN chmod +x /usr/local/bin/setup_gridengine.sh
#ADD configuration /etc/gridengine/configuration
#RUN chmod +x /etc/gridengine/configuration

#RUN useradd -m front_end --uid=2001 && echo "front_end:front_end" | \
#      chpasswd
#USER ${UID}:${GID}
#RUN useradd -m tool --uid=2002 && echo "tool:tool" | \
#      chpasswd

#CMD /usr/local/bin/setup_gridengine.sh && qconf -as sgemaster && echo "hostname ; date" | qsub && sleep 15 && qconf -as front_end.dockerized_vre_open-vre && tail -f /var/spool/gridengine/qmaster/messages
#CMD /usr/local/bin/setup_gridengine.sh && tail -f /var/spool/gridengine/qmaster/messages 
#CMD /usr/local/bin/setup_gridengine.sh && qconf -sconf > /tmp/configuration && sed 's/1000/0/g' /tmp/configuration > /etc/gridengine/configuration && sleep 15 && qconf -as front_end.dockerized_vre_open-vre && tail -f /var/spool/gridengine/qmaster/messages
#CMD /usr/local/bin/setup_gridengine.sh && sleep 15 && qconf -as front_end.dockerized_vre_open-vre && qconf -as sgetool.shared && tail -f /var/spool/gridengine/qmaster/messages
#CMD /usr/local/bin/setup_gridengine.sh && sleep 15 && qconf -as front_end.dockerized_vre_open-vre && tail -f /var/spool/gridengine/qmaster/messages
CMD /usr/local/bin/setup_gridengine.sh && qconf -as front_end.dockerized_vre_open-vre && tail -f /var/spool/gridengine/qmaster/messages

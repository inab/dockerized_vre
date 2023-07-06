FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && apt-get install -y gnupg2 vim

RUN echo 'deb http://deb.debian.org/debian/ buster main contrib non-free\n\
deb http://security.debian.org/debian-security/ buster/updates main contrib non-free\n' > /etc/apt/sources.list.d/debian.list

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys AA8E81B4331F7F50
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 112695A0E562B32A
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 04EE7237B7D453EC
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EF0F382A1A7B6500
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 648ACFD622F3D138
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0E98404D386FA1D9
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys DCC9EFBF77E11517

RUN apt-get update -y && apt-get install -y debian-archive-keyring

RUN apt-get update -y && apt-get install -y gridengine-exec gridengine-master gridengine-qmon
RUN ln -s /usr/share/gridengine/pixmaps /var/lib/gridengine/qmon/PIXMAPS

RUN apt-get update -y && apt-get install -y docker.io

RUN useradd -m application
RUN echo "application:application" | chpasswd

ADD setup_gridengine.sh /usr/local/bin/setup_gridengine.sh
RUN chmod +x /usr/local/bin/setup_gridengine.sh

CMD /usr/local/bin/setup_gridengine.sh && qconf -as front_end.dockerized_vre_open-vre && tail -f /var/spool/gridengine/qmaster/messages




FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3-pip git
RUN mkdir /home/openvre
WORKDIR /home/openvre
ADD requirements.txt requirements.txt
ADD receiver.py receiver.py
ADD src src
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt




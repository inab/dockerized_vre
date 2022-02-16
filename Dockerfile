# syntax=docker/dockerfile:1
FROM ubuntu:latest
#FROM python:3.7-alpine

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN git clone https://github.com/inab/openvre.git

RUN pwd

#COPY ./.:/usr/local/

#RUN git clone https://github.com/inab/openvre.git /usr/local/apache2/

#WORKDIR ./openvre

#ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0

#RUN apk add --no-cache gcc musl-dev linux-headers

#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt

#EXPOSE 5000
#COPY . .
#CMD ["flask", "run"]

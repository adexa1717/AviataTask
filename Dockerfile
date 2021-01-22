FROM python:3.8

MAINTAINER Adilzhan Berikkul <adexa1717@mail.ru>

WORKDIR /maindir
COPY maindir/ ./
RUN apt-get update && apt-get upgrade && apt-get install netcat -y
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

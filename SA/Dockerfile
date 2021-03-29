# Nome da imagem que servirá de base
FROM ubuntu:20.04
# Comandos que serão executados durante o 'docker build'
RUN apt-get update && apt-get install -y python3 && apt-get install -y python3-pip && apt-get install -y rabbitmq-server && rm -rf /var/lib/apt/lists/*
RUN pip3 install pika
RUN /etc/init.d/rabbitmq-server start

COPY main.py comunicacao_SS.py /
# Comando que será executado durante o 'docker run'


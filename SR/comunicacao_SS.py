import sys
import os
import subprocess
import pika
from time import sleep
import json
from threading import Thread

cmd = "hostname --all-ip-addresses|awk '{ print $1 }'"
ip = subprocess.check_output(["hostname", "--all-ip-addresses"])
ip2 = ip.split()

class ComunicacaoSS(Thread):

    def __init__(self, host):
        super(ComunicacaoSS, self).__init__()
        self.msg_rec = None
        credenciais = pika.PlainCredentials('std', 'std')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host), credentials=credenciais))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SS_para_SR')
        self.channel.queue_purge(queue='SS_para_SR')
        #print(' [*] Aguardando mensagens.')
        self.channel.basic_consume(queue='SS_para_SR', on_message_callback=self.proc_msg_rec)

        #robo vai se anunciar
        msg2 = "Nova conexao do robo: " + str(ip2[0])
        msg2 = json.dumps(msg2)
        self.channel.basic_publish(exchange='', routing_key='SR_para_SS', body=msg2)
        print("robo online com IP " + str(ip2[0]))

    def proc_msg_rec(self, ch, method, properties, body):
        self.msg_rec = body.decode()
        self.trata_msg_rec()

    def trata_msg_rec(self):
        msg = self.msg_rec
        msg2 = json.loads(msg)
        #print(msg)
        if 'moverPara' in msg2:
            #simular movimento
            print("Iniciando movimentacao")
            sleep(5)
            print("\nEm posicao")
            msg2 = "posicaoInicialAlcancada"
            try:
                self.channel.basic_publish(exchange='', routing_key='SR_para_SS', body=msg2)
            except:
                pass
        self.channel.queue_purge(queue='SS_para_SA')
        self.msg_rec = ""
        msg2 = ""
        sg = ""

    def run(self):
        self.channel.start_consuming()
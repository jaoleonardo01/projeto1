import sys
import os
import subprocess
import pika
from time import sleep
from threading import Thread

cmd = "hostname --all-ip-addresses|awk '{ print $1 }'"
ip = subprocess.check_output(["hostname", "--all-ip-addresses"])
ip2 = ip.split()

class ComunicacaoSR(Thread):

    def __init__(self, host):
        super(ComunicacaoSR, self).__init__()
        self.msg_rec = None
        credenciais = pika.PlainCredentials('std', 'std')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host), credentials=credenciais))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SR_para_SS', durable=False)
        print(' [*] Aguardando mensagens.')
        self.channel.basic_consume(queue='SR_para_SS', on_message_callback=self.proc_msg_rec)

    def proc_msg_rec(self, ch, method, properties, body):
        self.msg_rec = body.decode()
        self.trata_msg_rec()

    def trata_msg_rec(self):
        msg = self.msg_rec
        if 'Nova conexao do robo' in msg:
            msg2 = "Nova conexao do supervisor: " + str(ip2[0])
            try:
                sleep(0.1)
                #self.channel.basic_publish(exchange='', routing_key='SS_para_SA', body=msg2)
            except:
                pass
            self.channel.queue_purge(queue='SS_para_SA')

            msg = ""

    def run(self):
        self.channel.start_consuming()
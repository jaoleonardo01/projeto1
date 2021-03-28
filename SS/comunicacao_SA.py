import pika
import time
import json
import subprocess
from threading import Thread

global ip2

cmd = "hostname --all-ip-addresses|awk '{ print $1 }'"
ip = subprocess.check_output(["hostname", "--all-ip-addresses"])
ip2 = ip.split()

class ComunicacaoSA(Thread):

    def __init__(self, host):
        super(ComunicacaoSA, self).__init__()
        self.msg_rec = None
        credenciais = pika.PlainCredentials('std', 'std')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host), credentials=credenciais))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SA_para_SS2', durable=False)
        self.channel.queue_purge(queue='SA_para_SS2')
        print(' [*] Aguardando mensagens.')
        self.channel.basic_consume(queue='SA_para_SS2', on_message_callback=self.proc_msg_rec)

    def proc_msg_rec(self, ch, method, properties, body):
        self.msg_rec = body.decode()
        self.trata_msg_rec()

    def trata_msg_rec(self):
        msg = self.msg_rec
        msg2 = json.loads(msg)
        if 'novoJogo' in msg2:
            print("devemos enviar posicao inicial ao robo" + str(msg2))
        msg2 = ""
    def run(self):
        self.channel.start_consuming()
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
        self.channel.queue_declare(queue='SA_para_SS2')
        self.channel.queue_purge(queue='SA_para_SS2')
        self.channel.queue_purge(queue='SS_para_SA')
        print(' [*] Aguardando mensagens.')
        self.channel.basic_consume(queue='SA_para_SS2', on_message_callback=self.proc_msg_rec)

    def proc_msg_rec(self, ch, method, properties, body):
        self.msg_rec = body.decode()
        self.trata_msg_rec()

    def trata_msg_rec(self):
        msg = self.msg_rec
        msg2 = json.loads(msg)
        if 'novoJogo' in msg2:
            msg3 = "moverParaInicio",msg2[1],msg2[2]
            msg3 = json.dumps(msg3)
            self.channel.basic_publish(exchange='', routing_key='SS_para_SR', body=msg3)
            print("Enviado comando posicao inicial para o robo" + str(msg3))
            msg4 = "listaCacas",msg2[3],msg2[4],msg2[5],msg2[6],msg2[7],msg2[8]
            msg4 = json.dumps(msg4)
            #enviar lista de cacas para o SS
            self.channel.basic_publish(exchange='', routing_key='SR_para_SS', body=msg4)
            self.msg_rec = ""
            msg2 = ""
            msg = ""
            self.channel.queue_purge(queue='SA_para_SS2')

    def run(self):
        self.channel.start_consuming()
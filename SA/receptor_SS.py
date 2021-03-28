import pika
import time
import json
from transmissor_SS import *
from threading import Thread
from random import randint

global emJogo, caca, cacas
caca = {}
cacas = []

emJogo = False

class ReceptorSS(Thread):

    def __init__(self, host):

        self.coord_r1 = {0,0}
        self.r1_cacasEncontradas = []
        self.cacas = []
        super(ReceptorSS, self).__init__()
        self.msg_rec = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SS_para_SA')
        self.channel.queue_purge(queue='SS_para_SA')
        print(' [*] Aguardando mensagens.')
        self.channel.basic_consume(queue='SS_para_SA', on_message_callback=self.proc_msg_rec)

    def proc_msg_rec(self, ch, method, properties, body):
        self.msg_rec = body.decode()
        self.trata_msg_rec()

    # print(" [x] Received %r" % body.decode())
    # time.sleep(body.count(b'.'))
    # print(" [x] Done")
    # self.ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.start_consuming()

    def trata_msg_rec(self):
        msg = self.msg_rec
        if 'Nova conexao' in msg:
            emJogo = True
            self.gerarCacas()
            msg2 = "0","0",self.cacas[0]['x'],self.cacas[0]['y']
            msg2 = json.dumps(msg2)
            try:
                self.channel.basic_publish(exchange='', routing_key='SA_para_SS2', body=msg2)
            except:
                pass
            self.channel.queue_purge(SA_para_SS2)
            msg = ""

    def novoMapa(self):
        self.channel.start_consuming()

    def gerarCacas(self):
        for i in range(0, 5):
            caca["x"] = randint(1, 5)
            caca["y"] = randint(1, 5)
            self.cacas.append(caca)
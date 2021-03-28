import pika
from time import sleep
import json
from threading import Thread
from random import randint

global emJogo, caca, cacas,msg_rec
caca = {}
cacas = []

emJogo = False

class ComunicacaoSS(Thread):

    def __init__(self, host):

        self.coord_r1 = {0,0}
        self.r1_cacasEncontradas = []
        self.cacas = []
        self.gerarCacas()
        self.msg_rec = ""
        super(ComunicacaoSS, self).__init__()
        self.msg_rec = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SS_para_SA')
        self.channel.queue_purge(queue='SS_para_SA')
        self.channel.queue_purge(queue='SA_para_SS2')
        print(' [*] Aguardando mensagens.')
        self.channel.basic_consume(queue='SS_para_SA', on_message_callback=self.proc_msg_rec)

    def proc_msg_rec(self, ch, method, properties, body):
        self.msg_rec = body.decode()
        self.trata_msg_rec()

    def run(self):
        self.channel.start_consuming()

    def trata_msg_rec(self):
        msg = self.msg_rec
        if 'Nova conexao do supervisor' in msg:
            print(msg)
            print(cacas)
            msg2 = "novoJogo","A","0",self.cacas[0]['x'],self.cacas[0]['y'],self.cacas[1]['x'],self.cacas[1]['y'],self.cacas[2]['x'],self.cacas[2]['y']
            msg2 = json.dumps(msg2)
            self.channel.basic_publish(exchange='', routing_key='SA_para_SS2', body=msg2)
            self.channel.queue_purge(queue='SA_para_SS2')
            self.msg_rec = ""
            msg = ""

    def novoMapa(self):
        self.channel.start_consuming()

    def gerarCacas(self):
        for i in range(0, 2):
            lista = ['A', 'B', 'C', 'D', 'E', 'F']
            caca["x"] = lista[randint(0, 5)]
            caca["y"] = str(randint(1, 6))
            self.cacas.append(caca)
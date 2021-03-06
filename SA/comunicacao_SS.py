import pika
from time import sleep
import json
from threading import Thread
from random import randint

global emJogo, msg_rec,pontRobo1

emJogo = False

class ComunicacaoSS(Thread):

    def __init__(self, host):

        self.coord_r1 = {0,0}
        self.r1_cacasEncontradas = []
        self.cacas = [{'A','0'},{'A','0'},{'A','0'}]
        self.caca = {}
        self.gerarCacas()
        self.pontRobo1 = 0
        self.msg_rec = ""
        super(ComunicacaoSS, self).__init__()
        self.msg_rec = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SS_para_SA')
        self.channel.queue_purge(queue='SS_para_SA')
        #self.channel.queue_purge(queue='SA_para_SS2')
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
            print("\n" + msg)
            msg2 = "novoJogo","A","0",str(self.cacas['x1']), str(self.cacas['y1']),str(self.cacas['x2']), str(self.cacas['y2']),str(self.cacas['x3']), str(self.cacas['y3'])
            msg2 = json.dumps(msg2)
            self.channel.basic_publish(exchange='', routing_key='SA_para_SS2', body=msg2)
            self.channel.queue_purge(queue='SA_para_SS2')
            self.msg_rec = ""
            msg = ""

        if 'robo1PosicaoAlcancada' in msg:
            print("\nRobo 1 em posicao inicial  " + msg)

        if 'robo1CacaAlcancada' in msg:
            print("\nRobo 1 em posicao da CACA  " + msg)
            #validar cacas
            self.pontRobo1 = self.pontRobo1 +1
            if self.pontRobo1 == 3:
                print("\nPartida finalizada. Robo 1 encontrou as 3 cacas  ")
                self.channel.basic_publish(exchange='', routing_key='SA_para_SS2', body="FINALIZAR")
                self.connection.close()
                exit(-1)

    def novoMapa(self):
        self.channel.start_consuming()

    def gerarCacas(self):
        lista = ['A', 'B', 'C', 'D', 'E', 'F']
        x1 = lista[randint(0, 5)]
        y1 = randint(1, 6)
        x2 = lista[randint(0, 5)]
        y2 = randint(1, 6)
        x3 = lista[randint(0, 5)]
        y3 = randint(1, 6)
        self.cacas = {'x1': x1, 'y1': y1,'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3 }
        #for i in range(0, 3):
        #    x = lista[randint(0, 5)]
        #    y = str(randint(1, 6))
        #    self.cacas[i] = {x, y}
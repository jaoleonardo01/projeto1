import sys
import os
import subprocess
import pika
import json
from time import sleep
from threading import Thread

cmd = "hostname --all-ip-addresses|awk '{ print $1 }'"
ip = subprocess.check_output(["hostname", "--all-ip-addresses"])
ip2 = ip.split()

global listaCacas,proxAlvo, alvoX, alvoY

class ComunicacaoSR(Thread):

    def __init__(self, host):
        super(ComunicacaoSR, self).__init__()
        self.msg_rec = None
        credenciais = pika.PlainCredentials('std', 'std')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host), credentials=credenciais))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SR_para_SS')
        self.channel.queue_purge(queue='SR_para_SS')
        print(' [*] Aguardando mensagens.')
        self.channel.basic_consume(queue='SR_para_SS', on_message_callback=self.proc_msg_rec)

    def proc_msg_rec(self, ch, method, properties, body):
        self.msg_rec = body.decode()
        self.trata_msg_rec()

    def trata_msg_rec(self):
        msg = self.msg_rec
        if 'Nova conexao do robo' in msg:
            print("\n " + msg)
            msg2 = "Nova conexao do supervisor: " + str(ip2[0])
            try:
                self.channel.basic_publish(exchange='', routing_key='SS_para_SA', body=msg2)
            except:
                pass
            self.channel.queue_purge(queue='SS_para_SA')
            self.msg_rec = ""
            msg2 = ""
            msg = ""

        if 'listaCacas' in msg:
            msg5 = msg.split()
            self.listaCacas = {'x1':msg5[1],'y1':msg5[2],'x2':msg5[3],'y2':msg5[4],'x3':msg5[5],'y3':msg5[6]}
            #print(self.listaCacas)

        if 'posicaoInicialAlcancada' in msg:
            msg7 = "robo1PosicaoAlcancada " + msg[23] + msg[24]
            self.channel.basic_publish(exchange='', routing_key='SS_para_SA', body=msg7)
            print("\n Robo em posicao, iniciando caca..")
            self.alvoY = str(self.listaCacas.popitem())
            self.alvoX = str(self.listaCacas.popitem())
            self.alvoX = self.alvoX[9]
            self.alvoY = self.alvoY[9]
            msg3 = "moverParaCaca",self.alvoX,self.alvoY
            msg3 = json.dumps(msg3)
            print("\n Robo em deslocamento para caca: " + self.alvoX,self.alvoY)
            self.channel.basic_publish(exchange='', routing_key='SS_para_SR', body=msg3)

        if 'posicaoCacaAlcancada' in msg:
            if len(self.listaCacas) > 0:
                #validar caca com o SA
                msg4 = "robo1CacaAlcancada " + self.alvoX + self.alvoY
                msg4 = json.dumps(msg4)
                self.channel.basic_publish(exchange='', routing_key='SS_para_SA', body=msg4)
                print("\n Continuando caca..")
                self.alvoY = str(self.listaCacas.popitem())
                self.alvoX = str(self.listaCacas.popitem())
                self.alvoX = self.alvoX[9]
                self.alvoY = self.alvoY[9]
                msg3 = "moverParaCaca", self.alvoX, self.alvoY
                msg3 = json.dumps(msg3)
                print("\n Agora o alvo eh: " + self.alvoX, self.alvoY)
                self.channel.basic_publish(exchange='', routing_key='SS_para_SR', body=msg3)
            else:
                msg5 = "robo1CacaAlcancada " + self.alvoX + self.alvoY
                msg5 = json.dumps(msg5)
                self.channel.basic_publish(exchange='', routing_key='SS_para_SA', body=msg5)
                print("todas as cacas foram alcancadas")

        if 'FINALIZAR' in msg:
            self.channel.basic_publish(exchange='', routing_key='SS_para_SR', body="FINALIZAR")
            self.connection.close()
            exit(-1)

    def run(self):
        self.channel.start_consuming()
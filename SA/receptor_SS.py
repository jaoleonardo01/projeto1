import pika
import time
from transmissor_SS import *
from threading import Thread

class ReceptorSS(Thread):

    def __init__(self, host):
        super(ReceptorSS, self).__init__()
        self.msg_rec = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SS_para_SA')
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
            self.channel.basic_publish(exchange='', routing_key='SA_para_SS', body="Nova conexao aceita")
        else:
            self.channel.basic_publish(exchange='', routing_key='SA_para_SS', body="Nao entendi")
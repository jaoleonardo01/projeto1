import pika
import time
from threading import Thread


class ReceptorSA(Thread):

    def __init__(self, host):
        super(ReceptorSA, self).__init__()

        credenciais = pika.PlainCredentials('std', 'std')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host), credentials=credenciais))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SA_para_SS2', durable=False)
        print(' [*] Aguardando mensagens.')
        self.channel.basic_consume(queue='SA_para_SS2', on_message_callback=self.proc_msg_rec)

    def proc_msg_rec(self, ch, method, properties, body):
        msg_rec = body.decode()
        trata_msg_rec(msg_rec)

    # print(" [x] Received %r" % body.decode())
    # time.sleep(body.count(b'.'))
    # print(" [x] Done")
    # self.ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.start_consuming()


def trata_msg_rec(msg_rec):
    print(msg_rec)
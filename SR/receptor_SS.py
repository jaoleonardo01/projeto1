import pika
import time


class ReceptorSS():

    def __init__(self, host):
        super(ReceptorSR, self).__init__()

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SS_para_SR')
        print(' [*] Aguardando mensagens.')
        self.channel.basic_consume(queue='SS_para_SR', on_message_callback=self.proc_msg_rec)

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
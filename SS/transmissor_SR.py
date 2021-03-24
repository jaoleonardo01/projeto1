import pika
from time import sleep


class TransmissorSA():

    def __init__(self, host):

        self.credenciais = pika.PlainCredentials('std', 'std')
        self.parametros = pika.ConnectionParameters(host, 5672, '/', self.credenciais)
        self.conexao = pika.BlockingConnection(self.parametros)
        self.canal = self.conexao.channel()
        self.canal.queue_declare(queue='task_queue', durable=True)

    def enviar(self, mensagem):

        self.canal.basic_publish(exchange='', routing_key='task_queue', body=mensagem)
        self.conexao.close()

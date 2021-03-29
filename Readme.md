**Instituto Federal de Santa Catarina - Campus São José  
Engenharia de Telecomunicações    
Prof. Emerson Ribeiro de Mello  
STD29006 – Sistemas Distribuídos  
Aluno: João Leonardo Martins**  

## Projeto Prático 1:

Consiste em um jogo do tipo captura de bandeiras, onde um sistema gerenciador media uma partida a ser disputada entre robôs e seus sistemas gestores. 

A forma de comunicação escolhida foi através de Enfileiramento de Mensagem (AMQP Protocol), utilizando RabbitMQ e Pika Python. 

### Instruções para execução:

git clone https://github.com/STD29006-classroom/2020-02-projeto-pratico-01-jaoleonardo01
	
#### para executar o Auditor	

cd 2020-02-projeto-pratico-01-jaoleonardo01/SA

docker build -t std/sa_joao .

docker network create --driver bridge --subnet=172.31.31.0/24 rede-std_joao

docker run -dit --rm --name auditor std/sa_joao

docker network connect --ip 172.31.31.200 rede-std_joao auditor

docker container attach auditor

/etc/init.d/rabbitmq-server start;rabbitmqctl add_user std std; rabbitmqctl set_user_tags std administrator;rabbitmqctl set_permissions -p / std ".*" ".*" ".*"

python3 /main.py
	
####para executar o Supervisor

cd 2020-02-projeto-pratico-01-jaoleonardo01/SS

docker build -t std/ss_joao .

docker run -dit --rm --name supervisor --network rede-std_joao std/ss_joao

docker container attach supervisor

python3 /main.py

####para executar o Robô	
	
cd 2020-02-projeto-pratico-01-jaoleonardo01/SR

docker build -t std/sr_joao .

docker run -dit --rm --name robo --network rede-std_joao std/sr_joao

docker container attach robo

python3 /main.py

### Pontos funcionais

- Coordenadas para caças de forma aleatória
- Comunicação entre os três processos utilizando Pika Python para enviar mensagem ao broker (RabbitMQ) 

### Pontos de melhoria

- Apenas um robô/sistema auditor foi implementado - tornar o código escalável
- Dificuldades na criação da imagem do servidor RabbitMQ/Auditor: o serviço não inicializa automaticamente e deve ser executado manualmente, conforme passo a passo anterior
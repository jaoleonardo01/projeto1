import sys
import os
import socket
import subprocess
from transmissor_SS import *
from receptor_SS import *
from time import sleep

servidor = "10.0.0.29"

def main():
    tSS = TransmissorSS(servidor)
    rSS = ReceptorSS(servidor)
    rSS.run()

    cmd = "hostname --all-ip-addresses|awk '{ print $1 }'"
    ip = subprocess.check_output(["hostname", "--all-ip-addresses"])
    ip2 = ip.split()
    tSS = TransmissorSS("172.31.11.228")
    mensagem = "Nova conexao do robo: " + str(ip2[0])
    tSS.enviar(mensagem)


if __name__ == '__main__':
    main()

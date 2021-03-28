import sys
import os
import socket
import subprocess
from transmissor_SA import *
from transmissor_SR import *
from receptor_SA import *
from receptor_SR import *
from time import sleep

servidor = "10.0.0.29"

if __name__ == '__main__':
	tSA = TransmissorSA(servidor)
	tSR = TransmissorSR(servidor)
	rSR = ReceptorSR(servidor)
	rSR.start()
	rSA = ReceptorSA(servidor)
	rSA.start()

	cmd = "hostname --all-ip-addresses|awk '{ print $1 }'"
	ip = subprocess.check_output(["hostname", "--all-ip-addresses"])
	ip2 = ip.split()

	mensagem = "Nova conexao do supervisor: " + str(ip2[0])
	tSA.enviar(mensagem)
	while True:
		sleep(4)
		tSA.enviar(mensagem)
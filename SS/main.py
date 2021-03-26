import sys
import os
import socket
import subprocess
from transmissor_SA import *
from transmissor_SR import *
from receptor_SA import *
from receptor_SR import *
from time import sleep



if __name__ == '__main__':
	tSA = TransmissorSA("172.31.11.228")
	tSR = TransmissorSR("172.31.11.228")
	rSR = ReceptorSR("172.31.11.228")
	rSR.start()
	rSA = ReceptorSA("172.31.11.228")
	rSA.start()

	cmd = "hostname --all-ip-addresses|awk '{ print $1 }'"
	ip = subprocess.check_output(["hostname", "--all-ip-addresses"])
	ip2 = ip.split()

	mensagem = "Nova conexao do supervisor: " + str(ip2[0])
	tSA.enviar(mensagem)
	while True:
		sleep(4)
		tSA.enviar(mensagem)
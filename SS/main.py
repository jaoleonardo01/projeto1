import sys
import subprocess
import os
import commands
from transmissor_SA import *
from transmissor_SR import *
from receptor_SA import *
from receptor_SR import *
from time import sleep

def main():

	ip = commands.getoutput("hostname -i")
	tSA = TransmissorSA("172.31.11.228")
	mensagem = str(ip)
	tSA.enviar(mensagem)

if __name__ == '__main__':
	main()
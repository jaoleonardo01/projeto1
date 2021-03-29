import sys
import os
import socket
import subprocess
from comunicacao_SR import *
from comunicacao_SA import *
from time import sleep

servidor = "172.31.31.200"

if __name__ == '__main__':
	cSR = ComunicacaoSR(servidor)
	cSR.start()
	cSA = ComunicacaoSA(servidor)
	cSA.start()


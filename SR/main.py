import sys
import os
import socket
import subprocess
from comunicacao_SS import *
from time import sleep

servidor = "172.31.31.200"

def main():
    cSS = ComunicacaoSS(servidor)
    cSS.start()

if __name__ == '__main__':
    main()

import sys
import os
import socket
import subprocess
from comunicacao_SS import *
from time import sleep

servidor = "10.0.0.29"

def main():
    cSS = ComunicacaoSS(servidor)
    cSS.start()

if __name__ == '__main__':
    main()

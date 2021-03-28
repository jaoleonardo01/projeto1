import sys
import os
import socket
import subprocess
from comunicacao_SS import *
from time import sleep


def main():
    c = ComunicacaoSS("localhost")
    c.start()


if __name__ == '__main__':
    main()

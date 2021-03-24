import sys
import os
import socket
import subprocess
from receptor_SS import *
from transmissorSS import *
from time import sleep


def main():
    tSS = TransmissorSS("localhost")
    r = ReceptorSS("localhost")
    r.run()


if __name__ == '__main__':
    main()

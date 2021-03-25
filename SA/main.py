import sys
import os
import socket
import subprocess
from receptor_SS import *
from transmissor_SS import *
from time import sleep


def main():
    r = ReceptorSS("localhost")
    r.run()


if __name__ == '__main__':
    main()

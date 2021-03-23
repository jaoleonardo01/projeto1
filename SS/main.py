from transmissor_SA import *
from transmissor_SR import *
from receptor_SA import *
from receptor_SR import *
from time import sleep

def main():

	tSA = TransmissorSA("172.31.11.228")
	mensagem = "Ronaldo!"
	tSA.enviar(mensagem)

if __name__ == '__main__':
	main()
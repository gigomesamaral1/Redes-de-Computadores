import socket 
import sys
import threading
from functions_gestor import *


# Recieves in SERVER PORT the commands:
# 'SAIR' - 
# 'CONSULTAR_LOCAL' - 
# 'CONSULTAR_RECLAMACOES' - 
# 'CRIAR_SERVICOS' - 
# 'COBRANCA' -  
# 'TERMINAR_SERVICO' - 

#sockets communication parameters
SERVER_PORT = 12100
MSG_SIZE    = 1024

FILE_L = "locais.txt"
FILE_A = "atividades.txt"
FILE_C = "cidadaos.txt"
FILE_S = "servicos.txt"

#main code
threads = []


def server_function(client_socket, file_l, file_a, file_c):
	while True:
		client_msg = client_socket.recv(MSG_SIZE)
		msg_request = client_msg.decode().split()
		"msg_request = msg_request.split()"

		print('Mensagem recebida pelo cliente: ', msg_request)
		if(len(msg_request) == 0):
			server_msg = ERROR + INV_COMMAND + '\n'  

		else:
			command = msg_request[COMMAND]
			lock.acquire()
			if command == 'SAIR':
				server_msg = sair_cidade(client_socket, msg_request, file_l)
				lock.release()

			if command == 'CONSULTAR_LOCAL':
				server_msg = consultar_locais(client_socket, msg_request, file_l)
				lock.release()

			if command == 'CONSULTAR_RECLAMACOES':
				server_msg = consultar_reclamacoes(client_socket, file_l)
				lock.release()


			elif command == 'REGISTAR_SERVICOS':
				server_msg = registar_servicos(client_socket, msg_request, file_l)
				lock.release()

			elif command == 'COBRANCA':
				server_msg = cobranca(client_socket, msg_request, file_l, file_s)
				lock.release()

			elif command == 'TERMINAR_SERVICO':
				server_msg = terminar_servico(client_socket, msg_request)
				lock.release()

			else:
				server_msg =  ERROR + INV_COMMAND + '\n' 
				lock.release()


		server_msg = server_msg.encode()
		client_socket.send(server_msg)
	file_l.close()
	file_a.close()
	file_c.close()
	file_s.close()
	client_socket.close()
	sys.exit(0)

server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #to be able to exit with ctrl+c
server_sock.bind(('', SERVER_PORT))
server_sock.listen(5)
lock = threading.Lock()

file_l = open("locais.txt", "a+")
file_a = open("atividades.txt", "a+")
file_c = open("cidadaos.txt", "r")
file_s = open("servicos.txt", "r")



while True:

	client_socket, client_address = server_sock.accept()         
	client_handler = threading.Thread(
		target=server_function, 
		args=(client_socket, file_l, file_a, file_c,))      #creates the thread
	threads.append(client_handler)                          #adds to the thread list
	client_handler.start()                                  #starts client thread

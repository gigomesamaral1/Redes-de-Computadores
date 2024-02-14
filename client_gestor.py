import socket
import sys
import select
from signal import signal, SIGINT
from functions_gestor import EXIT, OK


#sockets communication parameters
SERVER_PORT = 12100
SERVER_IP   = "127.0.0.1"
MSG_SIZE = 1024


client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

inputs = [client_socket, sys.stdin]

def handler():
    client_msg = "SAIR"
    client_msg = client_msg.encode()
    client_socket.send(client_msg)
    print("A sair da cidade (sigint ou ctrl+c detetado)")
    server_msg = client_socket.recv(MSG_SIZE)
    server_request = server_msg.decode()
    print("\nMensagem recebida pelo servidor: ", server_request)
    if server_request == OK + EXIT:
        exit()
    
signal(SIGINT, handler)

while True:
  print("Introduza a mensagem para o servidor: ")
  ins, outs, exs = select.select(inputs,[],[])
  #select returns to the ins list who is waiting to read

  for i in ins:

    # i == sys.stdin - someone wrote in the console, let's read and send
    if i == sys.stdin:
        user_msg = sys.stdin.readline()
        client_msg = user_msg.encode()
        client_socket.send(client_msg)

    # i == sock - the server sent a message to the socket
    elif i == client_socket:
        server_msg = client_socket.recv(MSG_SIZE)
        server_request = server_msg.decode()
        print("\nMensagem recebida pelo servidor:", server_request)
        if server_request == OK + EXIT:
            exit()

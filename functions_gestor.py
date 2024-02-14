#constants definition
NULL = ''
SPACE = " "
NEW_LINE = "\n"

FILE_L = "locais.txt"
FILE_A = "atividades.txt"
FILE_C = "cidadao.txt"
FILE_S = "servicos.txt"


#message info
COMMAND  = 0
NOME = 1

#for locais
SOCKET = 0
ID_LOCAL = 1
NAME = 2
LOT = 3
RANKING = 4


#for servicos
SOCKET = 0
ID_SERVICO = 1
LOCAL = 2
TIPO_SERVICOS = 3
PRECO= 4


#return codes
OK    = '1: '
ID    = ': '
ERROR = '0 Erro: '
USAGE = 'Usage: '


#return sub-codes
INV_COMMAND = 'comando inválido\n'
EXIT        = 'saida da cidade com sucesso\n'
NO_INFO = 'sem informacao\n'
MISSING_INFO  = 'falta de informação\n'
TOO_MUCH_INFO = 'demasiada informação\n'
LOCAL_OK = 'local consultado com sucesso\n'
NO_LOCAL = 'local inexistente\n'
COMPLAIN_OK = 'reclamacao consultada com sucesso\n'
SERVICE_EXISTS = 'servico ja registado\n'
COBRANCA  = 'cobranca criada com sucesso\n' 
SERVICE_NONEXISTENT = 'servico nao registado' 
NO_DEBT = 'local sem saldo\n'  
CANC_SERVICO = 'servico terminado com sucesso\n'
REG_SERVICO = 'REGISTAR_SERVICO <nome_servico> <id_local> <tipo_servico> <preco> <id_servico>\n'
CON_RECLAMACOES = 'CONSULTAR RECLAMACOES <id_local>\n'
SERV_NONEXISTENCE = ' SERVICO INEXISTENTE\n'
NO_SERVICO = ' nao e responsavel de nenhum servico'
NOT_YOURS = ' nao e responsavel deste local'



servicos = {}

#generic functions
#message handling functions


def find_addr(addr):
	for key, val in list(servicos.items()):
		if val[SOCKET] == addr:
			return key
	return NULL
	

def find_id(id): 
	for key, val in list(servico.items()):
		if val[ID_SERVICO] == id:
			return key
	return NULL

def find_id_addr(addr):
	for key, val in list(locais.items()):
		if val[SOCKET] == addr:
			return val[ID_LOCAL]
	return NULL



def find_id_ativ(id, name): 
	for key, val in list(locais.items()):
		if key == name:
			for key2, val2 in list(val[ATIVS].items()):
				if val2[ID_ATIV] == id:
					return key2
	return NULL
	

def sair_cidade(client_socket, msg_request):
	if (len(msg_request) > 1):
		server_msg = ERROR + TOO_MUCH_INFO + USAGE + SAIR
	
	name = find_addr(client_socket)

	if (name == NULL):
		server_msg = OK + EXIT
	
	else:
		id = find_id_addr(client_socket)
		cancelar_local(client_socket, "CANCELAR_LOCAL" + str(id))
		server_msg = OK + EXIT
	
	return server_msg


def registar_servicos(client_socket, msg_request, file_l):
	if(len(msg_request) == 1):
			server_msg = ERROR + NO_INFO + USAGE + REG_SERVICO
	elif(len(msg_request) < 6):
			server_msg = ERROR + MISSING_INFO + USAGE + REG_SERVICO
	elif (len(msg_request) > 6):
		server_msg = ERROR + TOO_MUCH_INFO + USAGE + REG_SERVICO

	else:
		servico_name = msg_request[NOME]
		name = find_addr(client_socket)
		local = msg_request[LOCAL]
		tipo_servicos = msg_request[TIPO_SERVICOS]
		preco = msg_request[PRECO]

		if(servico_name in servicos):
			server_msg = ERROR + SERVICE_EXISTS

		elif(name != NULL):
			server_msg = ERROR + NO_LOCAL
		else:
			id_servico = len(servicos) + 1
			servicos[servico_name] = [client_socket, id_servico, tipo_servicos, int(preco), "0"]
			info = nome_servico + SPACE + str(id_local) + SPACE + tipo_servico + SPACE + preco + \
				SPACE + str(id_servico) + SPACE + "0" + NEW_LINE
			with open(FILE_L, "a") as file_id:
				file_id.write(info)
			server_msg = str(id_servico) + STR_ID + SERVICO_OK
	
	return server_msg
	
	
	


def consultar_locais(client_socket, msg_request, file_l):
	
	if (len(msg_request) > 1):
		server_msg = ERROR + "TOO MUCH INFO" + USAGE + LOCAL_OK
	else:
		name = find_id(client_socket)
		if (name == NULL):
			server_msg = ERROR + NO_LOCAL
		else:
			server_msg = str(locais[name][ID_LOCAL] + ' ' + locais[name][NAME] + ' ' + locais[name][LOT])



	

def consultar_reclamacoes(client_socket, msg_request):
	if(len(msg_request) > 1):
		server_msg = ERROR + TOO_MUCH_INFO + USAGE + CON_RECLAMACOES
		


def cobranca(client_socket, msg_request, file_l, file_s):
	if (len(msg_request) > 2):
		server_msg = ERROR + TOO_MUCH_INFO + USAGE + COBRANCA
	elif (len(msg_request) < 2):
		server_msg =  ERROR + MISSING_INFO + USAGE + COBRANCA

	else:
		id_servico = msg_request[ID_SERVICO]
		preco = msg_request[PRECO]

		if (id_servico in servicos):
			server_msg = "Servico encontrado"
		else:
			server_msg = "Servico nao encontrado"
		
   
	return(server_msg)


def terminar_servico(client_socket, msg_request):
    if (len(msg_request) == 1):
        server_msg = ERROR + NO_INFO + USAGE + CANC_SERVICO
    elif (len(msg_request) > 2):
        server_msg = ERROR + TOO_MUCH_INFO + USAGE + CANC_SERVICO
    else:
        id = msg_request[ID_SERVICO]
        servico_name = find_addr(client_socket)            
        closing_servico = find_id(int(id))
        if (servico_name == NULL):
            server_msg = ERROR + NO_SERVICO
        elif (closing_servico == NULL):
            server_msg = ERROR + SERV_NONEXISTENCE
        elif(local_name != closing_servico):
            server_msg = ERROR + NOT_YOURS
      
        else: 
            with open(FILE_A, "r") as file:
                lines = file.readlines()
            with open(FILE_A, "w") as file:
                for line in lines:
                    if not line.startswith(closing_servico):
                        file.write(line)
            
            with open(FILE_S, "r") as file:
                lines = file.readlines()
            with open(FILE_S, "w") as file:
                for line in lines:
                    if not line.startswith(id):
                        file.write(line)    

            servicos.pop(closing_servico)    

            server_msg = OK + CANC_SERVICO

    return server_msg

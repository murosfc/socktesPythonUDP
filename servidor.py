import socket
import datetime

UDP_IP = "127.0.0.1"
UDP_PORT_REC = 5005
UDP_PORT_SEND = 5010

#instancia das variáveis de socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT_REC))
sock.settimeout(10)

print("\nAguardando cliente conectar através da porta UDP: ", UDP_PORT_REC)

try:
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if data.decode() == "login": #prossegue se receber do cliente o identificador de login
            now = datetime.datetime.now()
            print ("\nHost logado atraves do IP: ", addr, "às", now.strftime("%H:%M:%S")) #imprime o endereço do host conectado ao servidor
            strLogado = "\n \n ****ESCOLHA UMA OPCAO ABAIXO**** \n1 - Verificar a hora no servidor \n2 - Encerrar a conexao. \n"
            sock.sendto(strLogado.encode(), (UDP_IP, UDP_PORT_SEND)) #envia o menu de opções ao cliente
            while True:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                opcao = int(data.decode()) #switch case para tratar a resposta do cliente ao menu enviado
                match opcao:
                    case 1: #Neste caso o cliente pediu para exibir a hora no servidor. que envia uma string codificada com essa informação e novamente o menu
                        now = datetime.datetime.now()
                        print("\ndata e hora enviada ao cliente: \n", addr)
                        horaString = "\nData e hora no servidor: " + now.strftime("%d/%m/%Y, %H:%M:%S") + "\n \n****ESCOLHA UMA OPCAO ABAIXO**** \n1 - Verificar data e hora no servidor \n2 - Encerrar a conexao. \n"
                        sock.sendto(horaString.encode(), (UDP_IP, UDP_PORT_SEND))
                    case 2:#Neste caso o cliente escolheu encerrar a conexão, o servidor envia a resposta e encerra a conexão
                        sock.sendto(b"Conexao encerrada", (UDP_IP, UDP_PORT_SEND))
                        sock.close()
                        now = datetime.datetime.now()
                        print("\nConexao encerrada", "às ", now.strftime("%H:%M:%S"))
                        quit()
                    case _: #Se a opção recebida for inválida o servidor comunica e encerra a conexão
                        sock.sendto(b"Opcao invalida. Conexao encerrada", (UDP_IP, UDP_PORT_SEND))
                        sock.close()
                        now = datetime.datetime.now()
                        print("\nConexao encerrada", "às ", now.strftime("%H:%M:%S"))
                        quit()
        else: #Encerra o programa caso não receba o pedido de login do cliente
            sock.close()
            print("Conexao encerrada")
            quit()
except TimeoutError:
    print ("Conexao encerrada por inatividade do cliente")
    sock.close()
    quit()
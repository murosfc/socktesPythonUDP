#importação da biblioteca socket
import socket
import datetime #bibliteca para trabalhar com data e hora

UDP_IP = "127.0.0.1" #constante para o endereço de ip do servidor de destino
UDP_PORT_SEND = 5005 #constante para a porta de envio de dados
UDP_PORT_REC = 5010 #constante para a porta de recebimento de dados

#instancia das variáveis de socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket.AF_INET identifica que estamos trabalhando Internet Protocol (IP)
sock.bind((UDP_IP, UDP_PORT_REC)) # Associa o socket a um endereço socket e uma porta
sock.settimeout(10) #tempo limite para receber a resposta do fornecedor = 10 segundos

#O servidor roda um programa que retorna a data e hora na máquina em que está rodando
print ("\nSolicitando programa ao servidor...")
#envia ao servidor a sitring de autenditação a letra b no inicio identifica que a string foi codificada
sock.sendto(b"login", (UDP_IP, UDP_PORT_SEND))

try: #bloco try para tratar exceção caso não receba resposta do servidor no tempo determinado
    while True:
        data, addr = sock.recvfrom(1024) #ativa o listener aguardando o servidor enviar as opções do menu
        if data: #caso tenha recebido algo do serividor o programa segue
            menu = input(data.decode()) #exibido o menu recebido do servidor após decodificar e guarda a resposta do usuário na variável menu
            sock.sendto(menu.encode(), (UDP_IP, UDP_PORT_SEND)) #envia ao servidor a resposta, novamente codificada
            while True:
                data, addr = sock.recvfrom(1024) #ativa o listener aguardando o servidor enviar a resposta
                if data.decode().find("Conexao encerrada") != -1: #se o retorno conter Conexão encerrada, o programa finaliza do lado do cliente
                    now = datetime.datetime.now()
                    print(data.decode(), "às ", now.strftime("%H:%M:%S")) #Decodifica e imprime a mensagem final do servidor
                    sock.close() #encerra o socket
                    quit() #encerra o programa
                else: #Se a solicitação foi da hora, o servidor envia novamente as opções ao usuário
                    menu = input(data.decode()) #exibido o menu recebido do servidor após decodificar e guarda a resposta do usuário na variável menu
                    sock.sendto(menu.encode(), (UDP_IP, UDP_PORT_SEND)) #envia ao servidor a resposta, novamente codificada
        else: #se não recebeu conteúdo em data, o programa encerra
            print ("\nFalha na conexao")
            quit()
except TimeoutError: #se não houver resposta do fornecedor no tempo estipulado o programa encerra
    print ("\nConexão encerrada por inatividade do servidor.")
    sock.close() #encerra o socket
    quit()


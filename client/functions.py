import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from datetime import datetime

def clear_screen():
    os.system('cls')

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Conexão encerrada pelo remetente.")
                break
            print("Recebido:", data.decode())
        except ConnectionResetError:
            print("Conexão encerrada pelo remetente.")
            break
        except Exception as e:
            print("Um erro ocorreu:", str(e))
            break
        
def menu():
    print("SPACE TRANSMITTER")
    print("1 - Cadastrar Sonda e Gerar Par de Chaves")
    print("2 - Enviar Chave da Sonda")
    print("3 - Coletar Dados da Sonda")
    print("4 - Gerar Assinatura dos dados Coletados")
    print("5 - Enviar para a terra os dados")
    print("6 - Cancelar transmissão")
    opcao = input("Escolha uma opção: ")
    return opcao

def gerar_chaves():
    nome_sonda = input("Digite o nome da Sonda: ").lower()
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    private_key_filename = f"{nome_sonda}.private.pem"
    public_key_filename = f"{nome_sonda}.public.pem"
    
    with open(private_key_filename, "wb") as priv_file:
        priv_file.write(private_key)
    with open(public_key_filename, "wb") as pub_file:
        pub_file.write(public_key)
    clear_screen()
    print(f"Chaves geradas e salvas como {private_key_filename} e {public_key_filename}!")


def enviar_chave(client_socket_b):
    nome_sonda = input("Digite o nome da Sonda para enviar sua chave pública: ").lower()
    public_key_filename = f"{nome_sonda}.public.pem"
    
    try:
        with open(public_key_filename, "rb") as pub_file:
            public_key = pub_file.read()
    except FileNotFoundError:
        clear_screen()
        print(f"Chave pública para a sonda {nome_sonda} não encontrada.")
        return
    
    client_socket_b.sendall(len(public_key_filename).to_bytes(4, 'big'))
    client_socket_b.sendall(public_key_filename.encode())
    client_socket_b.sendall(len(public_key).to_bytes(4, 'big'))
    client_socket_b.sendall(public_key)
    clear_screen()
    print(f"Chave pública da sonda {nome_sonda} enviada com sucesso!")

def coletar_dados():
    local = input("Local: ")
    temperatura = input("Temperatura: ")
    radiacao_alfa = input("Radiação Alfa: ")
    radiacao_beta = input("Radiação Beta: ")
    radiacao_gama = input("Radiação Gama: ")

    dados = f"Local: {local}\nTemperatura: {temperatura}\nRadiação Alfa: {radiacao_alfa}\nRadiação Beta: {radiacao_beta}\nRadiação Gama: {radiacao_gama}"

    data_atual = datetime.now().strftime("%d.%m")
    nome_arquivo = f"{local.replace(' ', '').lower()}{data_atual}.txt"

    chave = get_random_bytes(16)  
    iv = get_random_bytes(16)
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    dados_criptografados = cipher.encrypt(pad(dados.encode(), AES.block_size))

    with open(nome_arquivo, "wb") as arquivo:
        arquivo.write(iv + dados_criptografados)
    clear_screen()
    print(f"Os dados foram salvos em {nome_arquivo} e criptografados com sucesso!")

def assinar_dados():
    nome_arquivo = input("Digite o nome do arquivo de dados para assinar: ")
    nome_sonda = input("Digite o nome da sonda: ").lower()
    private_key_filename = f"{nome_sonda}.private.pem"

    nome_arquivo_completo = f"{nome_arquivo}.txt"
    
    try:
        with open(nome_arquivo_completo, "rb") as file:
            dados = file.read()
    except FileNotFoundError:
        clear_screen()
        print(f"Arquivo {nome_arquivo_completo} não encontrado.")
        return
    
    try:
        with open(private_key_filename, "rb") as key_file:
            private_key = RSA.import_key(key_file.read())
    except FileNotFoundError:
        clear_screen()
        print(f"Chave privada {private_key_filename} não encontrada.")
        return

    h = SHA256.new(dados)
    signature = pkcs1_15.new(private_key).sign(h)

    with open(f"{nome_arquivo}assinatura", "wb") as sign_file:
        sign_file.write(signature)
    clear_screen()
    print(f"Assinatura gerada e salva como {nome_arquivo}assinatura.")

def enviar_dados(client_socket_b):
    nome_arquivo = input("Digite o nome do arquivo de dados para enviar: ")
    nome_arquivo_completo = f"{nome_arquivo}.txt"
    nome_assinatura = f"{nome_arquivo}assinatura"
    
    try:
        with open(nome_arquivo_completo, "rb") as file:
            dados = file.read()
    except FileNotFoundError:
        clear_screen()
        print(f"Arquivo {nome_arquivo_completo} não encontrado.")
        return
    
    try:
        with open(nome_assinatura, "rb") as file:
            assinatura = file.read()
    except FileNotFoundError:
        clear_screen()
        print(f"Arquivo de assinatura {nome_assinatura} não encontrado.")
        return
    
    client_socket_b.sendall(len(nome_arquivo_completo).to_bytes(4, 'big'))
    client_socket_b.sendall(nome_arquivo_completo.encode())
    
    client_socket_b.sendall(len(dados).to_bytes(4, 'big'))
    client_socket_b.sendall(dados)
    
    client_socket_b.sendall(len(nome_assinatura).to_bytes(4, 'big'))
    client_socket_b.sendall(nome_assinatura.encode())

    client_socket_b.sendall(len(assinatura).to_bytes(4, 'big'))
    client_socket_b.sendall(assinatura)
    clear_screen()
    print("Dados e assinatura enviados com sucesso!")
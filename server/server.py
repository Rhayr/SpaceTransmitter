import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def verify_signature(data, signature, public_key):
    try:
        rsa_key = RSA.import_key(public_key)
        hash_data = SHA256.new(data)
        pkcs1_15.new(rsa_key).verify(hash_data, signature)
        return True  
    except (ValueError, TypeError):
        return False


def receive_messages(client_socket):
    while True:
        try:
            filename_size = int.from_bytes(client_socket.recv(4), 'big')
            filename = client_socket.recv(filename_size).decode()

            file_data_size = int.from_bytes(client_socket.recv(4), 'big')
            file_data = client_socket.recv(file_data_size)
            
            with open(f"{filename}", "wb") as file:
                file.write(file_data)
                
            print(f"Arquivo {filename} recebido e salvo com sucesso!")

            signature_filename_size = int.from_bytes(client_socket.recv(4), 'big')
            signature_filename = client_socket.recv(signature_filename_size).decode()
            
            signature_data_size = int.from_bytes(client_socket.recv(4), 'big')
            signature_data = client_socket.recv(signature_data_size)
            
            with open(f"{signature_filename}", "wb") as file:
                file.write(signature_data)
                
            print(f"Arquivo {signature_filename} recebido e salvo com sucesso!")

            sonda_name = input("Digite o nome da sonda para verificar a assinatura: ")
            public_key_filename = f"{sonda_name}.public.pem"

            try:
                with open(public_key_filename, "rb") as key_file:
                    public_key = key_file.read()
            except FileNotFoundError:
                print(f"Chave pública para a sonda {sonda_name} não encontrada.")
                print("Por gentileza, refaça o envio com os dados corretos.")
                continue  
            
            is_valid_signature = verify_signature(file_data, signature_data, public_key)
            
            if is_valid_signature:
                print("Dados e assinatura verificados com sucesso!")
            else:
                print("A assinatura não corresponde aos dados ou é inválida!")
                print("Por gentileza, se você tem certeza de ter colocado os dados corretos, reinicie a conexão e tente novamente. Estamos em manutenção.")

        except ConnectionResetError:
            print("Conexão encerrada pelo remetente.")
            break
        except Exception as e:
            print("Um erro ocorreu:", str(e))
            break

# Configurações do servidor/cliente A
HOST_A = "127.0.0.1"
PORT_A = 443

server_socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_a.bind((HOST_A, PORT_A))
server_socket_a.listen()

print("Aguardando conexões...")
client_socket_a, client_address_a = server_socket_a.accept()
print("Conexão estabelecida com:", client_address_a)

receive_thread = threading.Thread(target=receive_messages, args=(client_socket_a,))
receive_thread.start()

server_socket_a.close()

import socket
import threading
import functions  
HOST_B = '127.0.0.1'
PORT_B = 443

client_socket_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_b.connect((HOST_B, PORT_B))

receive_thread = threading.Thread(target=functions.receive_messages, args=(client_socket_b,))
receive_thread.start()

if __name__ == "__main__":
    while True:
        opcao = functions.menu()
        if opcao == "1":
            functions.gerar_chaves()
        elif opcao == "2":
            functions.enviar_chave(client_socket_b)
        elif opcao == "3":
            functions.coletar_dados()
        elif opcao == "4":
            functions.assinar_dados()
        elif opcao == "5":
            functions.enviar_dados(client_socket_b)
        elif opcao == "6":
            print("Encerrando o cliente...")
            client_socket_b.close()
            break
        else:
            print("Opção inválida.")

    client_socket_b.close()

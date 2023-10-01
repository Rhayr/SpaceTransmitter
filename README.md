# 🚀 Space Transmitter 
### 👩‍💻 Desenvolvido por Rhayra R. Fiorentin (RA: 1135147)

O Space Transmitter é um projeto de comunicação segura via sockets, desenvolvido como projeto acadêmico para a disciplina de Cybersecurity. Seu objetivo é estabelecer uma conexão segura entre um cliente e um servidor, possibilitando o envio de informações criptografadas para o servidor.

## 🌟 Principais Funcionalidades

- **Cadastro de sonda e geração de chaves**
- **Envio de chave para o servidor** 
- **Coleta de dados da sonda**
- **Geração de assinatura para os dados coletados**
- **Envio de dados para o servidor**
  
## 💻 Tecnologias Utilizadas

- **[Python](https://www.python.org/):** Linguagem de programação utilizada para o desenvolvimento do projeto.
- **[PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/):** Biblioteca de Python usada para criptografar as informações transmitidas.
- **[rsa](https://stuvel.eu/python-rsa-doc/):** Biblioteca que implementa o algoritmo RSA para a criação de assinaturas digitais.
  
## 📚 Pré-Requisitos

- Ter Python 3.x instalado.
- Ter as bibliotecas PyCryptodome e rsa instaladas.

## 🛠️ Execução

1. Clone este repositório para o seu sistema local ou baixe o ZIP.
2. Abra o terminal e navegue até o diretório onde o projeto está localizado.
3. No terminal execute os comandos `py server.py` e `py client.py`.

import json
import os
from cryptography.fernet import Fernet

# Carrega a chave do arquivo
def carregar_chave():
    with open("chave.key", "rb") as chave_arquivo:
        return chave_arquivo.read()

# Inicializa o objeto de criptografia
chave = carregar_chave()
fernet = Fernet(chave)

# Adiciona uma nova senha
def adicionar_senha(servico, usuario, senha):
    senha_criptografada = fernet.encrypt(senha.encode()).decode()

    if os.path.exists("senhas.json"):
        with open("senhas.json", "r") as arquivo:
            dados = json.load(arquivo)
    else:
        dados = {}

    dados[servico] = {
        "usuario": usuario,
        "senha": senha_criptografada
    }

    with open("senhas.json", "w") as arquivo:
        json.dump(dados, arquivo, indent=4)

    print(f"✅ Senha para '{servico}' salva com sucesso.")

# Mostra todas as senhas salvas
def ver_senhas():
    if not os.path.exists("senhas.json"):
        print("❌ Nenhuma senha salva ainda.")
        return

    with open("senhas.json", "r") as arquivo:
        dados = json.load(arquivo)

    if not dados:
        print("📭 Arquivo de senhas está vazio.")
        return

    print("\n📁 Senhas salvas:\n")
    for servico, info in dados.items():
        senha = fernet.decrypt(info["senha"].encode()).decode()
        print(f"🔒 Serviço: {servico}")
        print(f"👤 Usuário: {info['usuario']}")
        print(f"🔑 Senha: {senha}")
        print("-" * 30)

# Menu principal
def menu():
    while True:
        print("\n====== GERENCIADOR DE SENHAS ======")
        print("[1] Adicionar nova senha")
        print("[2] Ver senhas salvas")
        print("[3] Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            servico = input("Nome do serviço (ex: Gmail): ")
            usuario = input("Usuário ou email: ")
            senha = input("Senha: ")
            adicionar_senha(servico, usuario, senha)
        elif escolha == "2":
            ver_senhas()
        elif escolha == "3":
            print("👋 Saindo do programa...")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")

# Iniciar o programa
if __name__ == "__main__":
    menu()

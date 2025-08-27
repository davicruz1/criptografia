import json
import os
import base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

ARQUIVO_SENHAS = "senhas.json"
ARQUIVO_SALT = "salt.key"

# Deriva uma chave a partir de uma senha mestra
def carregar_chave():
    if not os.path.exists(ARQUIVO_SALT):
        salt = os.urandom(16)
        with open(ARQUIVO_SALT, "wb") as f:
            f.write(salt)
    else:
        with open(ARQUIVO_SALT, "rb") as f:
            salt = f.read()

    senha_mestra = getpass.getpass("Digite a senha mestra: ").encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    chave = base64.urlsafe_b64encode(kdf.derive(senha_mestra))
    return Fernet(chave)

fernet = carregar_chave()

def adicionar_senha(servico, usuario, senha):
    senha_criptografada = fernet.encrypt(senha.encode()).decode()

    if os.path.exists(ARQUIVO_SENHAS):
        with open(ARQUIVO_SENHAS, "r") as f:
            dados = json.load(f)
    else:
        dados = {}

    dados[servico] = {"usuario": usuario, "senha": senha_criptografada}

    with open(ARQUIVO_SENHAS, "w") as f:
        json.dump(dados, f, indent=4)

    print(f"✅ Senha para '{servico}' salva com sucesso.")

def ver_senhas():
    if not os.path.exists(ARQUIVO_SENHAS):
        print("❌ Nenhuma senha salva ainda.")
        return

    with open(ARQUIVO_SENHAS, "r") as f:
        dados = json.load(f)

    if not dados:
        print("📭 Nenhuma senha registrada.")
        return

    print("\n📁 Senhas salvas:\n")
    for servico, info in dados.items():
        senha = fernet.decrypt(info["senha"].encode()).decode()
        print(f"🔒 Serviço: {servico}")
        print(f"👤 Usuário: {info['usuario']}")
        print(f"🔑 Senha: {senha}")
        print("-" * 30)

def menu():
    while True:
        print("\n====== GERENCIADOR DE SENHAS ======")
        print("[1] Adicionar nova senha")
        print("[2] Ver senhas salvas")
        print("[3] Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            servico = input("Nome do serviço: ")
            usuario = input("Usuário/email: ")
            senha = getpass.getpass("Senha: ")
            adicionar_senha(servico, usuario, senha)
        elif escolha == "2":
            ver_senhas()
        elif escolha == "3":
            print("👋 Saindo...")
            break
        else:
            print("⚠️ Opção inválida.")

if __name__ == "__main__":
    menu()


from cryptography.fernet import Fernet
import os
os.system("clear")

def carregar_chave():
    """Carrega a chave a partir do arquivo chave.key"""
    return open('chave.key', 'rb').read()

def decriptar_mensagem(mensagem_encriptada, chave):
    """Decriptografa a mensagem usando a chave fornecida"""
    f = Fernet(chave)
    return f.decrypt(mensagem_encriptada.encode()).decode()

def main():
    chave = carregar_chave()
    
    # Solicita ao usuário a mensagem criptografada
    mensagem_encriptada = input("\n\n  \33[97m\33[1m[\33[93m\33[1m+\33[93m\33[1m\33[97m]\33[93m\33[1m MENSAGEM CRIPTOGRAFADA:\33[1m\33[97m ")
    
    try:
        mensagem_decriptada = decriptar_mensagem(mensagem_encriptada, chave)
        print("\n  \33[97m\33[1m[\33[93m\33[1m+\33[93m\33[1m\33[97m]\33[93m\33[1m INFO DECRIPTOGRAFADA:\33[1m\33[97m ", mensagem_decriptada)
    except Exception as e:
        print("\n  \33[97m\33[1m[\33[93m\33[1m+\33[93m\33[1m\33[97m]\33[93m\33[1m ERRO AO DECRIPTOGRAFAR:\33[1m\33[91m", mensagem_encriptada)

if __name__ == "__main__":
    main()

from cryptography.fernet import Fernet
from PIL import Image
import hachoir.metadata
import hachoir.parser
from hachoir.core import config as HachoirConfig
import piexif
import os
from __designer__ import __firstDesigner__
HachoirConfig.quiet = True
__firstDesigner__()
# Funções de Criptografia
def gerar_chave():
    chave = Fernet.generate_key()
    with open('chave.key', 'wb') as chave_arquivo:
        chave_arquivo.write(chave)

def carregar_chave():
    try:
        return open('chave.key', 'rb').read()
    except FileNotFoundError:
        print("Chave não encontrada. Gerando uma nova.")
        gerar_chave()
        return carregar_chave()

def criptografar_mensagem(mensagem):
    chave = carregar_chave()
    f = Fernet(chave)
    return f.encrypt(mensagem.encode())

# Funções de Manipulação de Metadados
def esconder_mensagem_metadados(imagem_path, mensagem_criptografada, saida_path):
    imagem = Image.open(imagem_path)
    
    if 'exif' in imagem.info:
        exif_dict = piexif.load(imagem.info['exif'])
    else:
        exif_dict = {'0th': {}, 'Exif': {}, 'GPS': {}, '1st': {}}
    
    # Adiciona a mensagem ao campo "UserComment"
    exif_dict['Exif'][0x9286] = mensagem_criptografada
    exif_bytes = piexif.dump(exif_dict)

    imagem.save(saida_path, exif=exif_bytes)

def ler_mensagem_metadados(imagem_path):
    imagem = Image.open(imagem_path)
    
    if 'exif' in imagem.info:
        exif_dict = piexif.load(imagem.info['exif'])
        return exif_dict['Exif'].get(0x9286, None)
    else:
        return None

# Função Principal
def main():
    if not os.path.isfile('chave.key'):
        gerar_chave()

    while True:
        print(" \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m 1 - ADICIONAR (SMS) METADADOS (JPG).")
        print(" \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m 2 - VISUALISAR METADATA (JPG).")
        print(" \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m 3 - SAIR.")
        opcao = input(" \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m [>>>\33[93m ")
        print ("\33[0m")
        if opcao == '1':
            #__firstDesigner__()
            imagem_path = input(" \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m IMAGE PATH (JPG):\33[93m ")
            mensagem = input(" \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m MENSAGEM PARA METADADOS:\33[93m ")
            mensagem_criptografada = criptografar_mensagem(mensagem)
            saida_path = input(" \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m PATH SAIDA DA IMAGEM (.jpg):\33[93m ")
            esconder_mensagem_metadados(imagem_path, mensagem_criptografada, saida_path)
            print("\n  \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m\33[0m\33[1m METADADOS MODIFICADOS COM SUCESSO.\n")

        elif opcao == '2':
            imagem_path = input(" \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m LER METADADOS IMAGE (JPG):\33[93m ")
            img_path = imagem_path
            filename = img_path
            parser = hachoir.parser.createParser(filename)
            hachoir_metadata = hachoir.metadata.extractMetadata(parser)
            metadata = hachoir_metadata.exportDictionary()['Metadata']
            if metadata is not None:
                print ("")
                for chave, valor in metadata.items():
                    print(f"   \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[97m\33[1m {repr(chave)}:\33[93m\33[1m {repr(valor)}")
                print ("")
                #print("Dados lidos dos metadados (mensagem criptografada):\n ", metadata)
            else:
                __firstDesigner__()
                print("  \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[91m\33[1m NENHUM METADADOS ENCONTRADO.")

        elif opcao == '3':
            __firstDesigner__()
            print("  \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[91m\33[1m SAINDO..")
            break

        else:
            __firstDesigner__()
            print("  \33[93m\33[1m[\33[97m\33[1m+\33[97m\33[1m\33[93m]\33[91m\33[1m OPÇÃO INVALIDADE TENTE NOVAMENTE.\n")

#if __name__ == "__main__":
#    main()

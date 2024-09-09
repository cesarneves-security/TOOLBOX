import os
import re
import time
import platform
import requests
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style, init
from __designer__ import __designerChoice__
from __designer__ import __miniDesigner__
from __designer__ import __miniDesigner2__
from __list__ import list_default
global list_defaultAll
# Inicializa colorama
#urlteste: https://www.hackertest.net
init()
os.system("clear")
__designerChoice__()
# Padrões de códigos maliciosos
padroes_maliciosos = [
    r'os\.system\(',  
    r'exec\(',        
    r'shell_exec\(',  
    r'include\(',     
    r'require\(',     
    r'eval\(',        
    r'preg_replace\(.+\/e',  
    r'\$_(GET|POST|COOKIE|SESSION)',  
    r'die\(',   
    r'exit\(',        
]

# Lista de extensões suspeitas
extensoes_suspeitas = []

class EventoMudancaArquivo(FileSystemEventHandler):
    def on_modified(self, event):
        print(Fore.RED + f" \33[1mFILE MODIFICADO: {event.src_path}" + Style.RESET_ALL)

def menu():
    print("\33[1m 1 - FILE-PATH")
    print(" 2 - DIRETORIO PATH")
    print(" 3 - ALL SYSTEM")
    print(" 4 - EM TEMPO REAL(DIRECTORY)")
    print(" 5 - EXTENSION MALWARE")
    print(" 6 - ANALISAR URL")
    print(" 7 - AJUDA(HELP)")
    escolha = input(" [$>>> ")
    print("")
    return escolha

def verificar_codigo_malicioso(conteudo):
    """Verifica se o conteúdo contém códigos maliciosos."""
    for padrao in padroes_maliciosos:
        if re.search(padrao, conteudo):
            return True
    return False

def analisar_arquivo(caminho_arquivo):
    """Analisa um arquivo específico em busca de código malicioso."""
    print(Fore.LIGHTYELLOW_EX + f" \33[1mANALISANDO FILES: {caminho_arquivo}" + Style.RESET_ALL)
    time.sleep(1)
    try:
        with open(caminho_arquivo, 'r', errors='ignore') as file:
            conteudo = file.read()
            
        if verificar_codigo_malicioso(conteudo):
            print(Fore.RED + f" \33[1mCÓDIGO MALICIOSO ENCONTRADO: {caminho_arquivo} {os.path.basename(caminho_arquivo)} {datetime.now()}" + Style.RESET_ALL)
    except Exception as e:
        print(f" \33[1m<.ERROR> ANALISE DE ARQUIVO: {caminho_arquivo}")

def analisar_diretorio(caminho_diretorio):
    """Analisa todos os arquivos em um diretório em busca de código malicioso."""
    for root, dirs, files in os.walk(caminho_diretorio):
        print(Fore.BLUE + f" \33[1mACESSANDO DIRECTORIO: {root}" + Style.RESET_ALL)
        for file in files:
            if file.split('.')[-1] in extensoes_suspeitas:
                caminho_arquivo = os.path.join(root, file)
                analisar_arquivo(caminho_arquivo)

def analisar_hd_sistema():
    """Analisa o HD do sistema em busca de arquivos maliciosos."""
    caminho_hd = "/" if platform.system() != "Windows" else "C:\\"
    print(Fore.BLUE + f" \33[1mANALISANDO SISTEMA RAIZ: {caminho_hd}" + Style.RESET_ALL)
    arquivos_encontrados = False

    for root, dirs, files in os.walk(caminho_hd):
        print(Fore.BLUE + f" \33[1mACESSANDO DIRECTORIO: {root}" + Style.RESET_ALL)
        for file in files:
            arquivos_encontrados = True
            if file.split('.')[-1] in extensoes_suspeitas:
                caminho_arquivo = os.path.join(root, file)
                analisar_arquivo(caminho_arquivo)

    if not arquivos_encontrados:
        print(" \33[1m<.ERROR> ARQUIVO NÃO ENCONTRADO.")

def analisar_url(url):
    """Analisa uma URL em busca de código malicioso."""
    print(Fore.LIGHTYELLOW_EX + f" \33[1mANALISANDO URL: {url}" + Style.RESET_ALL + f" \33[91m | {datetime.now()} | INATIVO ")
    time.sleep(1)
    try:
        response = requests.get(url)
        conteudo = response.text
        
        if verificar_codigo_malicioso(conteudo):
            print(Fore.RED + f"{url} | Ativo | SEGURO" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"{url} | Ativo | INFECTADO" + Style.RESET_ALL)
    except Exception as e:
        #print(f" \33[1m<.ERROR> ANÁLISE DA URL: {url}")
        pass

def iniciar_varredura_em_tempo_real(caminho_diretorio):
    """Inicia uma varredura em tempo real em um diretório."""
    event_handler = EventoMudancaArquivo()
    observer = Observer()
    observer.schedule(event_handler, caminho_diretorio, recursive=True)
    observer.start()
    os.system("clear")
    __miniDesigner__()
    print(f"\33[92m \33[1mANALISE EM TEMPO REAL INICIADA: {caminho_diretorio}"+"\33[0m")
    print()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def configurar_extensoes():
    """Configura extensões suspeitas para análise."""
    global extensoes_suspeitas
    extensoes = input(" \33[1mEXTENSÕES MALWARE'S (ex: .exe,.js,.php): ")
    extensoes_suspeitas = [ext.strip().lstrip('.') for ext in extensoes.split(',')]
    os.system("clear")
    __miniDesigner2__()
    print(f"\33[92m \33[1mEXTENSÕES SUSPEITAS CONFIGURADAS: {extensoes} \33[0m")
    print()

def mostrar_ajuda():
    """Exibe as instruções de uso do programa."""
    print("""\33[1m
    A J U D A:
          
    - Para analisar um arquivo específico, escolha a opção 1 e forneça o caminho do arquivo.
    - Para analisar todos os arquivos em um diretório, escolha a opção 2 e forneça o caminho do diretório.
    - Para analisar arquivos no HD do sistema, escolha a opção 3.
    - Para iniciar uma varredura em tempo real, escolha a opção 4 e forneça o diretório a ser monitorado.
    - Para configurar extensões suspeitas, escolha a opção 5 e forneça as extensões desejadas.
    - Para analisar uma URL, escolha a opção 6 e forneça a URL desejada.
    - Para acessar esta ajuda, escolha a opção 7.
    """)
    exit()

def main():
    """Função principal que controla o fluxo do programa."""
    while True:
        escolha = menu()
        if escolha == '1':
            caminho_arquivo = input(" \33[1mFILE PATH: ")
            analisar_arquivo(caminho_arquivo)
        elif escolha == '2':
            caminho_diretorio = input(" \33[1mDIRETORIO PATH: ")
            analisar_diretorio(caminho_diretorio)
        elif escolha == '3':
            analisar_hd_sistema()
        elif escolha == '4':
            caminho_diretorio = input(" \33[1mDIRECTORIO PATH/REAL: ")
            iniciar_varredura_em_tempo_real(caminho_diretorio)
        elif escolha == '5':
            configurar_extensoes()
        elif escolha == '6':
            url = input(" \33[1mDIGITE A URL: ")
            usar_lista = input(" \33[1mIMPORTAR DIRETORY LIST?(S/N) ")
            if usar_lista.lower() == 's':
                caminho_lista = input(" \33[1mDIGITE O CAMINHO DO ARQUIVO COM A LISTA: ")
                with open(caminho_lista, 'r') as file:
                    for linha in file:
                        url_diretorio = linha.strip()
                        analisar_url(url_diretorio)
            else:
                # Lista padrão de diretórios
                list_defaultAll = list_default
                for url_diretorio in list_defaultAll:
                    analisar_url(url_diretorio)
        elif escolha == '7':
            mostrar_ajuda()
        else:
            print(" \33[1m<.ERROR> OPÇÃO INVALIDA!")

#if __name__ == "__main__":
#    main()


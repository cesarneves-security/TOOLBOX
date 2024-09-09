import requests
from bs4 import BeautifulSoup
import re
import sys
from colorama import Fore, Style, init
from __designer__ import __designerSecond__
import os
import time

__designerSecond__()
print ("\33[1m")
# Inicializa o colorama
init(autoreset=True)
def carregar_lista_negra(arquivo):
    """Carrega URLs maliciosas de um arquivo .txt."""
    with open(arquivo, 'r') as f:
        return [linha.strip() for linha in f.readlines()]

def verificar_url_lista_negra(url, lista_negra):
    """Verifica se a URL está na lista negra."""
    if url in lista_negra:
        time.sleep(2)
        return Fore.RED + f" PHISHING < URL maliciosa identificada na lista negra {url_teste} >" + Style.RESET_ALL
    return None

def verificar_patterns(url):
    """Verifica a URL em busca de padrões suspeitos."""
    if re.search(r'[\\@\\%\\!\\=\\?]', url) or len(url) > 75:
        time.sleep(2)
        return Fore.YELLOW + f" POSSÍVEL < URL suspeita devido a padrões comuns {url_teste} >" + Style.RESET_ALL
    return None

def analisar_conteudo(url):
    """Analisa o conteúdo da página para sinais de phishing."""
    try:
        resposta = requests.get(url)
        soup = BeautifulSoup(resposta.content, 'html.parser')
        if soup.find('form'):
            time.sleep(2)
            return Fore.YELLOW + f" LOGIN DETECTADO < URL suspeita: contém um formulário de login: {url_teste} >" + Style.RESET_ALL
        return None
    except Exception as e:
        return f" ERRO DE ACESSO < Erro ao acessar a URL: {url_teste} >"

def verificar_url(url, lista_negra):
    """Verifica a URL usando todas as abordagens."""
    resultado = verificar_url_lista_negra(url, lista_negra)
    if resultado:
        time.sleep(2)
        return resultado
    
    resultado = verificar_patterns(url)
    if resultado:
        time.sleep(2)
        return resultado
    
    resultado = analisar_conteudo(url)
    if resultado:
        return resultado
    time.sleep(2)
    return Fore.WHITE + f" LINK LIMPO < URL aparentemente segura: {url_teste} >" + Style.RESET_ALL

if __name__ == "__main__":
    # Verifica se o nome do arquivo foi fornecido como argumento
    #if len(sys.argv) < 5:
    #    """ python __main__.py -U url_list.txt --url http://exemplo.com
	#        python __main__.py -D domain_list.txt --url http://exemplo.com
    #    """
    #    print(" Uso: python3 __main__.py -U url_list.txt --url <url>")
    #    print(" \33[1mUso: python3 __main__.py -D domain_list.txt --url <url>")
    #    sys.exit(1)

    confi = '-U'
    arquivo_lista_negra = input("  PATH WORDLIST URL MALICIONSO: ")
    confiURL = '--url'
    url_teste = input('  DEGITE URL MALICIOSA: ')

    # Carregar a lista negra a partir do arquivo fornecido
    lista_negra = carregar_lista_negra(arquivo_lista_negra)

    # Testar a função com a URL fornecida
    resultado = verificar_url(url_teste, lista_negra)
    print(resultado)
import os
import time
import random
import shutil
from colorama import Fore, Style, init

# Inicializa o colorama
init(autoreset=True)

def clear_terminal():
    # Limpa o terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_chuva_de_caracteres(linhas, colunas):
    # Lista de caracteres para usar
    caracteres = "!@#$%^&*()_+qwertyuiop[]{};':,.<>?/~`"
    
    while True:
        # Escolhe uma cor aleatória
        cor = random.choice([
            Fore.GREEN, 
            Fore.LIGHTGREEN_EX, 
            Fore.LIGHTYELLOW_EX, 
            Fore.CYAN
        ])
        
        # Gera múltiplos caracteres em posições aleatórias
        for _ in range(random.randint(1, 5)):  # Gera de 1 a 5 caracteres por iteração
            posicao = random.randint(0, colunas - 1)
            linha = random.randint(1, linhas)  # Garante que a linha esteja dentro do terminal
            char = random.choice(caracteres)
            
            # Move o cursor para a posição aleatória e imprime o caractere
            print(f"\033[{linha};{posicao}H{cor}{char}{Style.RESET_ALL}")
        
        # Reduz o tempo de espera para acelerar o efeito
        #time.sleep(0.01)  # Ajuste o valor para acelerar ou desacelerar

def main():
    # Obtendo as dimensões do terminal
    tamanho_terminal = shutil.get_terminal_size()
    linhas = tamanho_terminal.lines
    colunas = tamanho_terminal.columns

    clear_terminal()
    criar_chuva_de_caracteres(linhas, colunas)

if __name__ == "__main__":
    main()

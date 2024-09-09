import os
import time
from __designer__ import __designerFace__
from __scanface__ import *
__designerFace__()

if __name__ == "__main__":
    print ("\33[1m")
    target = input(" [Digite o IP/Domínio do Alvo]: ")
    # Tenta resolver o nome do domínio para um endereço IP
    try:
        resolved_target = socket.gethostbyname(target)
        main(resolved_target)
    except socket.gaierror:
        print(f'{Fore.YELLOW}Não foi possível resolver o domínio: {target}. Verifique se ele está correto.')
    except Exception as e:
        print(f'{Fore.YELLOW}Ocorreu um erro: {e}')
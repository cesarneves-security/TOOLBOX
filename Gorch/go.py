#importando framework
import os #importando os 
import sys #importando sys
import google #importando google
from googlesearch import search #importando de google
from design import __designGo__ #design
import socket #socket
from difflib import * #tratando erros
import urllib.request,urllib.parse,urllib.error #tratando erros
from urllib.parse import unquote #tratando erros
import requests #requests
import re #re
import time #time
#codando / programação orientado a objecto.
try:#try
    #criando class
    class __main_go__:#classe principal
        #criando funções
        def __init__(self):#definindo funçao default
            __designGo__()
    #herdando a classe principal __main_go__ para a class __gorch__
    class __gorch__(__main_go__):#classe secundaria
        #criando funções
        def __execute_gorch__(self):#funções
            #importando variaveis do arquivo main
            from main import NotUse1 #sem uso para configuração, mas muito necessario
            from main import Gourl #o que o usuario degitar
            from main import NotUse2#sem uso para configuração, mas muito necessario
            from main import num_stop #Númerototal de pesquisas
            from main import NotUse3#sem uso para configuração, mas muito necessario
            from main import file_save#nome do file para salvar as pesquisas
            from user_agent import escolha
            #convertendo string para números.
            num_code = int(num_stop)#convertendo.
            #adicionando variaveis para comparação de codigo na parte do user
            __configer__ = "--search {} --ns {} --file-name {}".format(Gourl,num_stop,file_save)#conf var
            __configer_choice__ = '{} {} {} {} {} {}'.format(NotUse1,Gourl,NotUse2,num_stop,NotUse3,file_save)#conf var
            #usando if e else: 
            if (__configer__ == __configer_choice__):#usando if
                #imprimindo informações
                print ('\033[1m'+"\n\033[96m <---------- GoRch ---------->\033[0m"+'\033[0m')
                print ('\033[1m'+"\033[96m [create]\033[0m \033[90m César Neves"+'\033[0m')#imprimindo
                print ('\033[1m'+"\033[96m [inform]\033[0m \033[90m PESQUISA: {}".format(Gourl)+'\033[0m')#imprimindo
                print ('\033[1m'+"\033[96m [inform]\033[0m \033[90m RESULTADOS: {}".format(num_stop)+'\033[0m')#imprimindo
                print ('\033[1m'+"\033[96m [inform]\033[0m \033[90m FILE: {}".format(file_save)+'\033[0m')#imprimindo
                print ('\033[1m'+"\n\033[96m <====================== RESULTADOS ======================>\033[0m\n"+'\033[0m')#imprimindo
                #os.system("clear")
                #usando try e except
                try: #try
                    #verficando modulo
                    from googlesearch import search #google
                #usanod exceptp
                except ImportError: #usando except error
                    #imprimindo erro de instalação  
                    print(" [x] <.erro> Framework 'google' não instalado.")#imprimindo
                    #usando o input para perguntar para o user se quer instalar ou não.
                    __choice__ = input(" [y] - PARA INSTALAR O FRAMEWORK.\n [N] - PARA CANCELAR.\n [?]: $> ")#input
                    #usando o if para copmparar as 2 variaveis e se forem igual, vai continuar
                    if (__choice__.lower() == 'y'):#if
                        #imprimindo informações de instalação
                        print (" [V] INSTALANDO FRAMEWORD 'google'.")#imprimindo
                        #usando método inapropriado para instalar uma biblioteca python
                        #os.system
                        os.system('pip install google')#usando os.system
                    #usando elif se não
                    elif (__choice__.lower() == 'n'):#elif
                        #imprimindo erro de não instalação do framework google
                        print (" [X] AVISO! CANCELANDO INSTALAÇAO.")#imprimindo
                #usando for para listar cada pesquisa e armazenar na variavel __pesquisado__
                for __pesquisado__ in search(Gourl, tld="co.in", num=num_code, stop=num_code, pause=0):#for
                    #criando um arquivo para ser armazenado todos os dados da pesquisa 
                    arquivo = open('{}'.format(file_save), 'a')#criando o arquivo e abrindo
                    os.system('chmod 777 {}'.format(file_save))
                    #escrevendo todos os dados da informação
                    arquivo.writelines("{}\n".format(__pesquisado__))#salvando os dados da pesquisa
                    #imprimindo op resultado da pesquisas
                    __domain__ = __pesquisado__.split('//')[-1].split('/')[0]
                    ip_server = socket.gethostbyname(__domain__)
                    #USER-AGENT
                    headers = {'User-Agent': escolha}
                    __certificado__ = 'cacert.pem'
                    __url_response__ = requests.get(__pesquisado__, headers=headers, verify=__certificado__)
                    __xss__js_script__ = re.compile(r"<script>.*?</script>")
                    __html_injector_script__ = re.compile(r"<h1>.*?</h1>")
                    __check_vulnerabilidade__ = re.findall(__xss__js_script__, __url_response__.text) 
                    __check_vulnerabilidade2__ = re.findall(__html_injector_script__, __url_response__.text)

                    print('\033[1m'+"\n [+] "+__pesquisado__+'\033[0m')#imprimindo
                    print ("\033[96m        [-] DOMAIN:\033[36m {}".format(__domain__))
                    print ("\033[96m        [-] IP:\033[36m {}".format(ip_server))
                    print ("\033[96m        [-] USER-AGENT:\033[36m {}".format(escolha))
                    print ("\033[96m        [-] CERTIFICADO LOCAL:\033[36m {}".format(__certificado__))
                    #('\033[97m'+"OLÁ PYTHON3"+'\033[0m')
                    if (len(__check_vulnerabilidade2__) > 0):
                        print ("\033[96m        [-] HTML-INJECTION:\033[93m Yes/Potencial \033[0m")
                        for __vulnerabilidade2__ in __check_vulnerabilidade2__:
                            print ("\033[36m        [-] CODE: {} \033[0m".format(__vulnerabilidade2__))
                    else:
                        print ("\033[96m        [-] HTML-INJECTION:\033[91m NÃO \033[0m")

                    if (len(__check_vulnerabilidade__) > 0):
                        print ("\033[36m        [-] XSS:\033[93m Yes/Potencial \033[0m\n")
                        for __vulnerabilidade__ in __check_vulnerabilidade__:
                            print ("\033[36m        [+] XSS TESTING...: {}\033[0m".format(__vulnerabilidade__))
                    else:
                        print ("\033[96m        [-] XSS: \033[91m NÃO \033[0m")
                    time.sleep(1)
            #usando else
            else:#else
                #chamando a função.
                __designGo__()#função
                #imprimindo erro de pepsquisa
                print (" [x] <.erro> ERRO DE PESQUISA, TENTE NOVAMENTE.")#imprimindo
except urllib.error.URLError:
    __designGo__()
    os.system('clear')
    print ("\n [X] ERRO: ERRO DE CONNEXÃO.\n")
    exit()
except requests.exceptions.SSLError:
    __designGo__()
    os.system('clear')
    print ("\n [X] ERRO: [SSL: CERTIFICATE_VERIFY_FAILED].\n")
    exit()
except socket.gaierror:
    __designGo__()
    os.system('clear')
    print ("\n [X] ERRO: SERVER DESCONHECIDO..\n")
    exit()
#END

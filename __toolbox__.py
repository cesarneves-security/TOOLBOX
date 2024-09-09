# Vamos começar a comentar o código.
""" 
    VAMOS COMEÇAR A COMENTAR
    Nome: César neves
    Ft: TOOLBOX PRO
"""
from __designer__ import __config__
from __configure__ import __listToolbox__
import os
import time
import subprocess
import sys
class __main__():
    def __init__(self):
        __config__()
class __executeClass__(__main__):
    def __execute__(self):
        #condigo principal
        __listToolbox__()
        while True:
            __choiceTools__ = input ("\n   \33[1m\33[97m>>> \33[93m")
            if (__choiceTools__ == '14'):
                __config__()
                print ("    \33[1m\33[91mSAINDO...")
                time.sleep(1)
                break

            elif (__choiceTools__ == '1'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '1. ARSP-REDE'...\n")
                time.sleep(2)
                __config__()
                caminho1 = os.path.abspath('./ARSPREDE')
                os.chdir(caminho1)
                subprocess.run(["python", "__main__.py"])

            elif (__choiceTools__ == '2'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '2. CRIPTOWARE'...\n")
                time.sleep(2)
                __config__()
                # Caminho para o diretório onde está o __main__.py
                caminho = os.path.abspath("./Criptoware")
                # Muda o diretório de trabalho
                os.chdir(caminho)
                # Executa o __main__.py
                subprocess.run(["python", "__main__.py"])

            elif (__choiceTools__ == '3'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '3. GORCH'...\n")
                time.sleep(2)
                __config__()
                caminho2 = os.path.abspath('./Gorch')
                os.chdir(caminho2)
                subprocess.run(["python", "main.py"])

            elif (__choiceTools__ == '4'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '4. MALCRIPT'...\n")
                time.sleep(2)
                __config__()
                caminho3 = os.path.abspath('./MALCRIPT')
                os.chdir(caminho3)
                subprocess.run(["python", "index.py"])
            
            elif (__choiceTools__ == '5'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '5. METACRIPT'...\n")
                time.sleep(2)
                __config__()
                caminho4 = os.path.abspath('./Metacript')
                os.chdir(caminho4)
                subprocess.run(["python", "__main__.py"])

            elif (__choiceTools__ == '6'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '6. NAP'...\n")
                time.sleep(2)
                __config__()
                caminho5 = os.path.abspath('./NAP')
                os.chdir(caminho5)
                subprocess.run(["python", "__main__.py"])

            elif (__choiceTools__ == '7'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '7. NETDEFENDER'...\n")
                time.sleep(2)
                __config__()
                caminho6 = os.path.abspath('./NetDefender')
                os.chdir(caminho6)
                subprocess.run(["python", "cli.py"])

            elif (__choiceTools__ == '8'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '8. SCANFACE'...\n")
                time.sleep(2)
                __config__()
                caminho7 = os.path.abspath('./SCANFACE')
                os.chdir(caminho7)
                subprocess.run(["python", "__index__.py"])
            
            elif (__choiceTools__ == '9'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '9. SHELLINJECTOR'...\n")
                time.sleep(2)
                __config__()
                caminho8 = os.path.abspath('./ShellInjector')
                os.chdir(caminho8)
                subprocess.run(["python", "__main__.py"])
            
            elif (__choiceTools__ == '10'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '10. TD-THREATDETECT'...\n")
                time.sleep(2)
                __config__()
                caminho9 = os.path.abspath('./TD-ThreatDetect')
                os.chdir(caminho9)
                subprocess.run(["python", "__main__.py"])
            
            elif (__choiceTools__ == '11'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '11. VERYFILE'...\n")
                time.sleep(2)
                __config__()
                caminho10 = os.path.abspath('./VERYFILE')
                os.chdir(caminho10)
                subprocess.run(["python", "__main__.py"])
            
            elif (__choiceTools__ == '12'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '12. VWEB'...\n")
                time.sleep(2)
                __config__()
                caminho11 = os.path.abspath('./VWEB')
                os.chdir(caminho11)
                subprocess.run(["python", "vweb.py"])
            
            elif (__choiceTools__ == '13'):
                print ("\n   \33[1m\33[93mINICIANDO TOOL '13. EFFECTS'...\n")
                time.sleep(2)
                __config__()
                caminho12 = os.path.abspath('./EFFECTS')
                os.chdir(caminho12)
                subprocess.run(["python", "index.py"])

            else:
                print ("\n    \33[1m\33[91m<.ERROR COMANDO: '{}' NÃO ENCONTRADO...".format(__choiceTools__))
                time.sleep(2)
                __config__()
                __listToolbox__()
                


#if __name__ == "__main__":
#    __execute_config__ = __executeClass__()
#    __execute_config__.__execute__()


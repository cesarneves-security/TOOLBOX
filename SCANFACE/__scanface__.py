import socket
import paramiko
from ftplib import FTP
import pymysql
from smb.SMBConnection import SMBConnection
import subprocess
from colorama import init, Fore, Style
import requests

# Inicializa o colorama
init(autoreset=True)
print ("\33[1m")
# Lista de usernames default
usernames_default = ['admin', 'root', 'user', 'guest']

# Lista de passwords default
passwords_default = ['admin', 'root', 'user', 'guest', '123456', 'password']

# Dicionários de versões vulneráveis para cada serviço
vulnerable_versions = {
    'SSH': {
        'OpenSSH 7.2': 'Vulnerabilidade CVE-2016-0777',
        'OpenSSH 5.9': 'Vulnerabilidade CVE-2014-1692',
        'OpenSSH 6.0': 'Vulnerabilidade CVE-2016-0778',
        'OpenSSH 6.7': 'Vulnerabilidade CVE-2015-5600',
        'OpenSSH 6.8': 'Vulnerabilidade CVE-2016-10012',
        'OpenSSH 7.1': 'Vulnerabilidade CVE-2016-0778',
        'OpenSSH 7.3': 'Vulnerabilidade CVE-2017-15906',
        'OpenSSH 7.4': 'Vulnerabilidade CVE-2017-15906',
        'OpenSSH 7.5': 'Vulnerabilidade CVE-2017-15906',
        'Dropbear SSH 2016.74': 'Backdoor na versão',
    },
    'FTP': {
        'vsftpd 2.3.4': 'Backdoor na versão',
        'ProFTPD 1.3.5': 'Vulnerabilidade CVE-2015-3306',
        'Pure-FTPd 1.0.49': 'Vulnerabilidade CVE-2017-14108',
        'FileZilla Server 0.9.60': 'Vulnerabilidade CVE-2018-14602',
        'vsftpd 2.3.3': 'Vulnerabilidade CVE-2011-2523',
        'ProFTPD 1.3.6': 'Vulnerabilidade CVE-2015-3306',
        'Pure-FTPd 1.0.50': 'Vulnerabilidade CVE-2017-14108',
        'Pure-FTPd 1.0.48': 'Vulnerabilidade CVE-2016-6480',
        'vsftpd 3.0.3': 'Vulnerabilidade CVE-2015-3242',
        'FileZilla 3.31.0': 'Vulnerabilidade CVE-2017-6766',
    },
    'MySQL': {
        'MySQL 5.7.12': 'Vulnerabilidade CVE-2016-6662',
        'MySQL 5.6.27': 'Vulnerabilidade CVE-2016-6662',
        'MySQL 5.5.52': 'Vulnerabilidade CVE-2016-6662',
        'MySQL 8.0.11': 'Vulnerabilidade CVE-2017-3580',
        'MySQL 5.7.17': 'Vulnerabilidade CVE-2017-3303',
        'MySQL 5.7.19': 'Vulnerabilidade CVE-2017-3303',
        'MySQL 5.6.31': 'Vulnerabilidade CVE-2017-3303',
        'MySQL 5.5.60': 'Vulnerabilidade CVE-2017-3303',
        'MySQL 5.7.14': 'Vulnerabilidade CVE-2017-3303',
        'MariaDB 10.2.8': 'Vulnerabilidade CVE-2017-3697',
    },
    'SMB': {
        'SMB 1.0': 'Vulnerabilidade EternalBlue',
        'SMB 2.0': 'Vulnerabilidade CVE-2017-0144',
        'SMB 2.1': 'Vulnerabilidade CVE-2017-0144',
        'SMB 3.0': 'Vulnerabilidade CVE-2017-0144',
        'Windows Server 2008': 'Vulnerabilidade CVE-2017-0144',
        'Windows 7 SP1': 'Vulnerabilidade CVE-2017-0144',
        'Windows 8.1': 'Vulnerabilidade CVE-2017-0144',
        'Windows 10': 'Vulnerabilidade CVE-2017-0144',
        'Windows Server 2012': 'Vulnerabilidade CVE-2017-0144',
        'Windows Server 2016': 'Vulnerabilidade CVE-2017-0144',
    },
    'HTTP': {
        'Apache 2.4.49': 'Vulnerabilidade CVE-2021-41773',
        'Nginx 1.21.0': 'Vulnerabilidade CVE-2021-23017',
        'IIS 10.0': 'Vulnerabilidade CVE-2021-28480',
        'Lighttpd 1.4.59': 'Vulnerabilidade CVE-2021-32757',
    },
    'HTTPS': {
        'Apache 2.4.49': 'Vulnerabilidade CVE-2021-41773',
        'Nginx 1.21.0': 'Vulnerabilidade CVE-2021-23017',
        'IIS 10.0': 'Vulnerabilidade CVE-2021-28480',
        'Lighttpd 1.4.59': 'Vulnerabilidade CVE-2021-32757',
    }
}

# Função para escanear portas
def scan_ports(target, ports):
    open_ports = []
    for port in sorted(ports):  # Ordena as portas em ordem crescente
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
        except socket.error as e:
            print(f'{Fore.YELLOW}Erro ao conectar na porta {port}: {e}')
        sock.close()
    return open_ports

# Função para obter a versão do serviço
def get_service_version(target, port, service_name):
    try:
        if service_name == 'SSH':
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(target, username='root', password='admin', timeout=1)
            stdin, stdout, stderr = ssh_client.exec_command('ssh -V')
            version = stdout.read().decode().strip()
            ssh_client.close()
            return version if version else "Versão não encontrada"
        elif service_name == 'FTP':
            ftp = FTP(target)
            version = ftp.getwelcome()
            ftp.quit()
            return version if version else "Versão não encontrada"
        elif service_name == 'MySQL':
            connection = pymysql.connect(host=target, user='root', password='admin', connect_timeout=1)
            version = connection.get_server_info()
            connection.close()
            return version if version else "Versão não encontrada"
        elif service_name == 'SMB':
            command = "smbclient -V"
            result = subprocess.check_output(command, shell=True).decode().strip()
            return result if result else "Versão não encontrada"
        elif service_name in ['HTTP', 'HTTPS']:
            response = requests.get(f'http://{target}' if service_name == 'HTTP' else f'https://{target}', timeout=1)
            return response.headers.get('Server', 'Versão não encontrada')
    except Exception as e:
        print(f'{Fore.YELLOW}Erro ao obter a versão do serviço {service_name} na porta {port}: {e}')
        return "Versão não encontrada"

# Função para testar SSH
def test_ssh(target, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(target, username=username, password=password)
        print(f'{Fore.GREEN}SSH Login bem-sucedido: {username}:{password} - **Vulnerável**')
        client.close()
        return True
    except Exception:
        print(f'{Fore.RED}SSH: {username}:{password} - **Não Vulnerável**')
        return False

# Função para testar FTP
def test_ftp(target, username, password):
    try:
        ftp = FTP(target)
        ftp.login(user=username, passwd=password)
        print(f'{Fore.GREEN}FTP Login bem-sucedido: {username}:{password} - **Vulnerável**')
        ftp.quit()
        return True
    except Exception:
        print(f'{Fore.RED}FTP: {username}:{password} - **Não Vulnerável**')
        return False

# Função para testar MySQL
def test_mysql(target, username, password):
    try:
        connection = pymysql.connect(host=target, user=username, password=password)
        print(f'{Fore.GREEN}MySQL Login bem-sucedido: {username}:{password} - **Vulnerável**')
        connection.close()
        return True
    except Exception:
        print(f'{Fore.RED}MySQL: {username}:{password} - **Não Vulnerável**')
        return False

# Função para testar SMB
def test_smb(target, username, password):
    try:
        conn = SMBConnection(username, password, "client_machine", "server_machine", use_ntlm_v2=True)
        conn.connect(target)
        print(f'{Fore.GREEN}SMB Login bem-sucedido: {username}:{password} - **Vulnerável**')
        conn.close()
        return True
    except Exception:
        print(f'{Fore.RED}SMB: {username}:{password} - **Não Vulnerável**')
        return False

# Função para verificar o firewall
def check_firewall(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    sock.close()
    return result != 0

# Função principal
def main(target):
    print("\n===================================")
    print("         Início do Escaneamento     ")
    print("===================================")

    ports_to_scan = [22, 21, 3306, 445, 80, 443]  # SSH, FTP, MySQL, SMB, HTTP, HTTPS
    open_ports = scan_ports(target, ports_to_scan)

    print("\n===================================")
    print("          Portas Abertas           ")
    print("===================================")

    if not open_ports:
        print(f'Nenhuma porta aberta encontrada em {target}.')
        return

    for port in open_ports:
        service_name = 'Desconhecido'
        if port == 22:  # SSH
            service_name = 'SSH'
        elif port == 21:  # FTP
            service_name = 'FTP'
        elif port == 3306:  # MySQL
            service_name = 'MySQL'
        elif port == 445:  # SMB
            service_name = 'SMB'
        elif port == 80:  # HTTP
            service_name = 'HTTP'
        elif port == 443:  # HTTPS
            service_name = 'HTTPS'

        print(f'Porta {port} - {service_name}')

    vulnerabilities_found = []

    for port in open_ports:
        if port == 22:  # SSH
            print("\n===================================")
            print("           Teste de SSH            ")
            print("===================================")
            version = get_service_version(target, port, 'SSH')
            print(f'Versão do SSH: {version}')
            if version in vulnerable_versions['SSH']:
                vulnerabilities_found.append(f'SSH: {version} - **Vulnerável**: {vulnerable_versions["SSH"][version]}')
            else:
                print(f'SSH: {version} - **Sem Vulnerabilidades Conhecidas**')

            print(f'Testando SSH na porta {port}...\n')
            for username in usernames_default:
                for password in passwords_default:
                    test_ssh(target, username, password)

        elif port == 21:  # FTP
            print("\n===================================")
            print("           Teste de FTP            ")
            print("===================================")
            version = get_service_version(target, port, 'FTP')
            print(f'Versão do FTP: {version}')
            if version in vulnerable_versions['FTP']:
                vulnerabilities_found.append(f'FTP: {version} - **Vulnerável**: {vulnerable_versions["FTP"][version]}')
            else:
                print(f'FTP: {version} - **Sem Vulnerabilidades Conhecidas**')

            print(f'Testando FTP na porta {port}...\n')
            for username in usernames_default:
                for password in passwords_default:
                    test_ftp(target, username, password)

        elif port == 3306:  # MySQL
            print("\n===================================")
            print("           Teste de MySQL          ")
            print("===================================")
            version = get_service_version(target, port, 'MySQL')
            print(f'Versão do MySQL: {version}')
            if version in vulnerable_versions['MySQL']:
                vulnerabilities_found.append(f'MySQL: {version} - **Vulnerável**: {vulnerable_versions["MySQL"][version]}')
            else:
                print(f'MySQL: {version} - **Sem Vulnerabilidades Conhecidas**')

            print(f'Testando MySQL na porta {port}...\n')
            for username in usernames_default:
                for password in passwords_default:
                    test_mysql(target, username, password)

        elif port == 445:  # SMB
            print("\n===================================")
            print("           Teste de SMB            ")
            print("===================================")
            version = get_service_version(target, port, 'SMB')
            print(f'Versão do SMB: {version}')
            if version in vulnerable_versions['SMB']:
                vulnerabilities_found.append(f'SMB: {version} - **Vulnerável**: {vulnerable_versions["SMB"][version]}')
            else:
                print(f'SMB: {version} - **Sem Vulnerabilidades Conhecidas**')

            print(f'Testando SMB na porta {port}...\n')
            for username in usernames_default:
                for password in passwords_default:
                    test_smb(target, username, password)

        elif port == 80:  # HTTP
            print("\n===================================")
            print("           Teste de HTTP           ")
            print("===================================")
            version = get_service_version(target, port, 'HTTP')
            print(f'Versão do HTTP: {version}')
            if version in vulnerable_versions['HTTP']:
                vulnerabilities_found.append(f'HTTP: {version} - **Vulnerável**: {vulnerable_versions["HTTP"][version]}')
            else:
                print(f'HTTP: {version} - **Sem Vulnerabilidades Conhecidas**')

            print(f'Testando HTTP na porta {port}...\n')

        elif port == 443:  # HTTPS
            print("\n===================================")
            print("           Teste de HTTPS          ")
            print("===================================")
            version = get_service_version(target, port, 'HTTPS')
            print(f'Versão do HTTPS: {version}')
            if version in vulnerable_versions['HTTPS']:
                vulnerabilities_found.append(f'HTTPS: {version} - **Vulnerável**: {vulnerable_versions["HTTPS"][version]}')
            else:
                print(f'HTTPS: {version} - **Sem Vulnerabilidades Conhecidas**')

            print(f'Testando HTTPS na porta {port}...\n')

    # Verificação de Firewall
    print("\n===================================")
    print("         Verificação de Firewall    ")
    print("===================================")
    for port in ports_to_scan:
        if check_firewall(target, port):
            print(f'Porta {port} está **bloqueada** pelo firewall.')
        else:
            print(f'Porta {port} está **aberta** e acessível.')

    # Relatório de Vulnerabilidades
    print("\n===================================")
    print("         Relatório de Vulnerabilidades ")
    print("===================================")
    for vulnerability in vulnerabilities_found:
        print(vulnerability)

    print("\n===================================")
    print("          Escaneamento Concluído    ")
    print("===================================\n")

#if __name__ == "__main__":
#    target = input("Digite o IP ou o Domínio do Alvo: ")
#
#    # Tenta resolver o nome do domínio para um endereço IP
#    try:
#        resolved_target = socket.gethostbyname(target)
#        main(resolved_target)
#    except socket.gaierror:
#        print(f'{Fore.YELLOW}Não foi possível resolver o domínio: {target}. Verifique se ele está correto.')
#    except Exception as e:
#        print(f'{Fore.YELLOW}Ocorreu um erro: {e}')
#
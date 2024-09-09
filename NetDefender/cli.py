import json
import os
from scapy.all import *
from collections import defaultdict
import time
from __designer__ import __desenho__
__desenho__()#chamando a função desenho
#print ("\33[1m")
# Classe para representar uma regra
class Rule:
    def __init__(self, action, protocol, port, source_ip):
        self.action = action
        self.protocol = protocol
        self.port = port
        self.source_ip = source_ip

    def __str__(self):
        return f"{self.action} {self.protocol} {self.port} {self.source_ip}"

# Classe para gerenciar o firewall
class Firewall:
    def __init__(self):
        self.rules = []
        self.suspicious_ips = {}
        self.connection_attempts = defaultdict(int)
        self.blocked_ips = set()
        self.ddos_protection_limit = 100  # Limite de requisições para DDoS
        self.ddos_block_time = 60  # Tempo (em segundos) que o IP ficará bloqueado
        self.ddos_blocked_ips = {}  # Dicionário para armazenar bloqueios temporários

    def add_rule(self, rule):
        for existing_rule in self.rules:
            if (existing_rule.action == rule.action and
                existing_rule.protocol == rule.protocol and
                existing_rule.port == rule.port and
                existing_rule.source_ip == rule.source_ip):
                #print("Regra já existe:", existing_rule)
                return  # Não adicionar a regra se já existir
        self.rules.append(rule)
        #print("Regra adicionada:", rule)

    def remove_rule(self, rule_str):
        for rule in self.rules:
            if str(rule) == rule_str:
                self.rules.remove(rule)
                print("\33[1m   REGRAS REMOVIDAS.", rule)
                return
        print("\33[1m\33[97m   REGRAS NÃO ENCONTRADAS.\33[0m\n")

    def list_rules(self):
        if not self.rules:
            print("\33[1m NENHUMA REGRA CONFIGURADA.")
        else:
            __desenho__()
            print("\33[1m REGRAS DO FIREWALL:\n")
            for rule in self.rules:
                print(f"   \33[96m{rule}\33[0m")
            print ("")

    def log_event(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_message = f"{timestamp}: {message}\n"
        with open("firewall_logs.txt", "a") as log_file:
            log_file.write(log_message)

    def start(self):
        __desenho__()
        print("\33[1m\33[96m FIREWALL LIGADO: INICIANDO MONITORAMENTO E DEFESA: NETDEFENDER.\33[0m")
        time.sleep(1)
        sniff(prn=self.process_packet, filter="ip", store=0)

    def process_packet(self, packet):
        if packet.haslayer(IP):
            ip_src = packet[IP].src
            protocol = packet.proto
            port = packet[IP].dport if packet.haslayer(TCP) or packet.haslayer(UDP) else None
            
            # Verificar se o IP está bloqueado
            if ip_src in self.blocked_ips:
                return  # Bloquear o pacote

            # Incrementar contagem de tentativas de conexão
            self.connection_attempts[ip_src] += 1

            # Verificar se o IP está temporariamente bloqueado por DDoS
            if ip_src in self.ddos_blocked_ips:
                unblock_time = self.ddos_blocked_ips[ip_src]
                if time.time() < unblock_time:
                    return  # IP ainda está bloqueado
                else:
                    del self.ddos_blocked_ips[ip_src]  # Remover bloqueio se o tempo passou

            # Verificar se o IP é suspeito e registrar
            if self.connection_attempts[ip_src] > 20 and ip_src not in self.suspicious_ips:
                self.suspicious_ips[ip_src] = time.time()
                protocol_type = "TCP" if protocol == 6 else "UDP" if protocol == 17 else "Unknown"
                print(f"\33[1m\033[91m   Atividade suspeita detectada de {ip_src} usando protocolo {protocol_type}. Bloqueando IP.\033[0m")
                self.log_event(f"Atividade suspeita detectada de {ip_src} usando protocolo {protocol_type}. Bloqueio aplicado.")
                self.blocked_ips.add(ip_src)  # Bloquear IP suspeito
                return

            # Detectar DDoS
            if self.connection_attempts[ip_src] > self.ddos_protection_limit:
                print(f"\33[1m\033[91m   Ataque DDoS detectado de {ip_src}. Bloqueando IP por {self.ddos_block_time} segundos.\033[0m")  # Impressão em vermelho
                self.blocked_ips.add(ip_src)
                self.ddos_blocked_ips[ip_src] = time.time() + self.ddos_block_time  # Bloquear temporariamente
                self.log_event(f"Ataque DDoS detectado de {ip_src}. Bloqueio aplicado.")
                return  # IP bloqueado

            # Verificar regras configuradas
            for rule in self.rules:
                if rule.source_ip == ip_src and rule.protocol.lower() == str(protocol).lower() and (port == int(rule.port) or rule.port == "any"):
                    if rule.action == "deny":
                        self.log_event(f"Pacote bloqueado: {rule}")
                        return  # Bloquear o pacote
                    elif rule.action == "allow":
                        self.log_event(f"Pacote permitido: {rule}")
                        return  # Permitir o pacote

# Funções para carregar e salvar configurações
CONFIG_FILE = 'config.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"rules": []}  # Retorna uma configuração vazia se o arquivo não existir

    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

def save_config(firewall):
    rules_list = []
    for rule in firewall.rules:
        rules_list.append({
            "action": rule.action,
            "protocol": rule.protocol,
            "port": rule.port,
            "source_ip": rule.source_ip
        })
    
    with open(CONFIG_FILE, 'w') as file:
        json.dump({"rules": rules_list}, file, indent=4)
        __desenho__()
    print("\33[1m\33[97m CONFIGURAÇÕES SALVAS COM SUCESSO.\33[0m\n")

# Função para imprimir o menu
def print_menu():
    print("\33[1m NETDEFENDER CONFIG:\n")
    print("   1 - VISUALIZAR REGRAS.")
    print("   2 - CRIAR REGRAS.")
    print("   3 - DELETAR REGRAS.")
    print("   4 - SALVAR CONFIGURAÇÕES.")
    print("   5 - START NETDEFENDER.")
    print("   6 - EXIT\n")

# Função principal
def main():
    firewall = Firewall()
    config = load_config()

    # Carregar regras do arquivo de configuração
    for rule in config["rules"]:
        new_rule = Rule(rule["action"], rule["protocol"], rule["port"], rule["source_ip"])
        firewall.add_rule(new_rule)

    # Regras padrão (exemplo)
    default_rules = [
        Rule("deny", "TCP", "23", "any"),  # Bloquear Telnet
        Rule("deny", "TCP", "21", "any"),  # Bloquear FTP
        Rule("allow", "TCP", "80", "any"),  # Permitir HTTP
        Rule("allow", "TCP", "443", "any")  # Permitir HTTPS
    ]
    for rule in default_rules:
        firewall.add_rule(rule)

    while True:
        print_menu()
        command = input("\33[1m   [command]: ")
        
        if command == "1":
            firewall.list_rules()

        elif command == "2":
            __desenho__()
            print (" \33[1mCRIAR REGRAS:\n")
            action = input("   ACTION (allow/deny): ")
            protocol = input("   PROTOCOLO: ")  # Agora aceita qualquer protocolo
            port = input("   PORTA: ")
            source_ip = input("   IP DE ORIGEM: ")
            __desenho__()
            print (f" \33[96m\33[1mREGRA CRIADA COM SUCESSO: {source_ip} => ({protocol}):{port}\33[0m\n")
            new_rule = Rule(action, protocol, port, source_ip)
            firewall.add_rule(new_rule)

        elif command == "3":
            __desenho__()
            print (" \33[91m\33[1mDELETAR REGRAS:")
            rule_str = input("   REMOVENDO CONFIGURAÇÕES (formato: ação protocolo porta IP): \33[0m")
            firewall.remove_rule(rule_str)

        elif command == "4":
            save_config(firewall)

        elif command == "5":
            firewall.start()  # Iniciar o firewall

        elif command == "6":
            __desenho__()
            save_config(firewall)  # Salvar configurações antes de sair
            print("\33[1m\33[96m SAINDO..")
            break

        else:
            __desenho__()
            print(f"\33[1m\33[91m COMANDO: '{command}' INVALIDO.\33[0m\n")

if __name__ == "__main__":
    main()

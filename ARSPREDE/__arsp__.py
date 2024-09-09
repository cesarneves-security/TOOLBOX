# Importando as bibliotecas necessárias
#***Nome: César Neves***
from scapy.all import sniff, IP, ICMP
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QVBoxLayout
from collections import defaultdict
import sys
import threading
import time
from __designer__ import __designerText__
__designerText__()
# Definindo o limite de alerta configurável
ALERT_THRESHOLD = 20  # Altere este valor conforme necessário

# Dicionário para armazenar o tráfego de IPs
ip_traffic = defaultdict(lambda: {'sent': 0, 'received': 0})
protocol_traffic = defaultdict(int)  # Para armazenar tráfego por protocolo
response_times = []  # Para armazenar os tempos de resposta
total_packets = 0  # Contador total de pacotes
capturing = True  # Flag para controle de captura de pacotes

# Função para exibir um alerta ao usuário
def show_alert(ip):
    print(f"\033[91mAtenção: O IP {ip} ultrapassou o limite de pacotes! Total Enviados: {ip_traffic[ip]['sent']}\033[0m")

# Função de callback para processar pacotes capturados
def packet_callback(packet):
    global total_packets
    #Sem Falar do Rews que tem Cabeça grande
    if IP in packet:
        ip_src = packet[IP].src  # Endereço IP de origem
        ip_dst = packet[IP].dst  # Endereço IP de destino
        protocol = packet[IP].proto  # Protocolo
        # Contar pacotes enviados e recebidos por IP
        ip_traffic[ip_src]['sent'] += 1
        ip_traffic[ip_dst]['received'] += 1
        # Contagem de pacotes por protocolo
        protocol_traffic[protocol] += 1
        #o Keidi é Ainda mais Burros.
        # Adicionar tempo de resposta para pacotes ICMP
        if ICMP in packet:
            # Usar uma abordagem diferente para capturar o tempo de resposta
            # Aqui você pode usar um timestamp de quando o pacote foi enviado, se disponível
            response_times.append(time.time())  # Apenas adiciona o tempo atual como exemplo
        # Atualiza o total de pacotes
        total_packets += 1
        # Imprimir detalhes do pacote capturado
        print(f"\033[1mPacote capturado: Src={ip_src}, Dst={ip_dst}, Proto={protocol}, Total Enviados={ip_traffic[ip_src]['sent']}")
        # Verificar se há atividade suspeita
        if ip_traffic[ip_src]['sent'] == ALERT_THRESHOLD + 1:  # Alerta quando ultrapassa o limite
            show_alert(ip_src)  # Chama a função de alerta

# Classe para a aplicação principal com PyQt5
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARSP REDE - Gráficos de Tráfego")
        self.setGeometry(100, 100, 1400, 900)  # Tamanho da janela aumentado

        # Layout principal
        layout = QGridLayout()

        # Criando os canvases para os gráficos com tamanho fixo
        self.canvas_ip_traffic = FigureCanvas(Figure(figsize=(10, 6)))  # Aumentando o tamanho dos gráficos
        self.canvas_protocol_traffic = FigureCanvas(Figure(figsize=(10, 6)))
        self.canvas_total_packets = FigureCanvas(Figure(figsize=(10, 6)))
        self.canvas_error_packets = FigureCanvas(Figure(figsize=(10, 6)))

        # Adicionando os canvases ao layout com proporções
        layout.addWidget(self.canvas_ip_traffic, 0, 0)  # Gráfico de tráfego de IPs
        layout.addWidget(self.canvas_protocol_traffic, 0, 1)  # Gráfico de protocolos
        layout.addWidget(self.canvas_total_packets, 1, 0)  # Gráfico de tráfego total
        layout.addWidget(self.canvas_error_packets, 1, 1)  # Gráfico de pacotes com erro

        # Adicionando botões
        self.pause_button = QPushButton("Pausar Análise")
        self.pause_button.setStyleSheet("background-color: red; color: white;")
        self.pause_button.clicked.connect(self.pause_analysis)

        self.start_button = QPushButton("Iniciar Análise")
        self.start_button.setStyleSheet("background-color: green; color: white;")
        self.start_button.clicked.connect(self.start_analysis)

        # Layout para os botões
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button)  # Botão de iniciar análise
        button_layout.addWidget(self.pause_button)  # Botão de pausar análise

        # Adicionando o layout dos botões ao layout principal
        layout.addLayout(button_layout, 0, 2)  # Coluna direita para os botões

        # Configurando o widget central e o layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Iniciar a captura de pacotes em uma thread separada
        threading.Thread(target=capture_packets, args=(100,), daemon=True).start()

        # Iniciar a atualização dos gráficos
        self.timer = threading.Timer(1.0, self.update_graphs)
        self.timer.start()

    def update_graphs(self):
        if capturing:  # Atualiza os gráficos apenas se a captura estiver ativa
            self.update_ip_traffic_graph()
            self.update_protocol_graph()
            self.update_total_traffic_graph()
            self.update_error_graph()
        self.timer = threading.Timer(1.0, self.update_graphs)
        self.timer.start()

    def pause_analysis(self):
        global capturing
        capturing = False  # Pausa a captura

    def start_analysis(self):
        global capturing
        capturing = True  # Inicia a captura

    def update_ip_traffic_graph(self):
        ax = self.canvas_ip_traffic.figure.add_subplot(111)
        ax.clear()
        # Criar DataFrame para tráfego de IPs
        traffic_df = pd.DataFrame.from_dict(ip_traffic, orient='index')
        if not traffic_df.empty:  # Verifica se o DataFrame não está vazio
            traffic_df['suspect'] = traffic_df['sent'] > ALERT_THRESHOLD  # Coluna para IPs suspeitos
            # Definindo as cores para cada série
            colors_sent = ['red' if row['suspect'] else 'blue' for _, row in traffic_df.iterrows()]
            colors_received = ['black' if row['suspect'] else 'orange' for _, row in traffic_df.iterrows()]
            # Criar gráfico de barras com cores separadas
            bar_width = 0.35  # Largura das barras
            index = range(len(traffic_df))
            # Gráfico de pacotes enviados
            ax.bar(index, traffic_df['sent'], bar_width, color=colors_sent, label='Pacotes Enviados')
            # Gráfico de pacotes recebidos
            ax.bar([i + bar_width for i in index], traffic_df['received'], bar_width, color=colors_received, label='Pacotes Recebidos')
            # Adicionando informações no gráfico
            ax.set_title('Tráfego de IPs')
            ax.set_xlabel('Endereço IP (Src e Dst)')
            ax.set_ylabel('Número de Pacotes')
            ax.axhline(y=ALERT_THRESHOLD, color='red', linestyle='--', label='Limite Suspeito')
            ax.set_xticks([i + bar_width / 2 for i in index])
            ax.set_xticklabels(traffic_df.index, rotation=45)
            ax.legend()
            ax.set_ylim(0, traffic_df[['sent', 'received']].max().max() + 10)  # Ajusta o limite do eixo Y

            # Adicionando anotações para IPs suspeitos
            for i, (ip, row) in enumerate(traffic_df.iterrows()):
                if row['suspect']:
                    ax.text(i, row['sent'] + 1, 'Suspeito', color='red', ha='center', fontsize=10)
                    ax.text(i + bar_width, row['received'] + 1, 'Suspeito', color='black', ha='center', fontsize=10)
        self.canvas_ip_traffic.draw()
#meu amigo Adilson é muito burro
    def update_protocol_graph(self):
        ax = self.canvas_protocol_traffic.figure.add_subplot(111)
        ax.clear()
        # Criar gráfico de barras para protocolos
        ax.bar(protocol_traffic.keys(), protocol_traffic.values(), color='green')
        ax.set_title("Distribuição de Pacotes por Protocolo")
        ax.set_xlabel("Protocolos")
        ax.set_ylabel("Número de Pacotes")
        # Verifica se há valores no protocolo antes de definir o limite do eixo Y
        if protocol_traffic:
            ax.set_ylim(0, max(protocol_traffic.values()) + 10)  # Ajusta o limite do eixo Y
        else:
            ax.set_ylim(0, 10)  # Define um limite padrão
        # Formatar os eixos para mostrar apenas inteiros
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
        self.canvas_protocol_traffic.draw()

    def update_total_traffic_graph(self):
        ax = self.canvas_total_packets.figure.add_subplot(111)
        ax.clear()
        ax.bar(['Total de Pacotes'], [total_packets], color='blue')
        ax.set_title("Tráfego Total de Pacotes")
        ax.set_ylabel("Número Total de Pacotes")
        ax.set_ylim(0, total_packets + 10)  # Ajusta o limite do eixo Y
        # Formatar os eixos para mostrar apenas inteiros
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
        self.canvas_total_packets.draw()

    def update_error_graph(self):
        ax = self.canvas_error_packets.figure.add_subplot(111)
        ax.clear()
        error_packets = sum(1 for packet in ip_traffic.values() if packet['sent'] < 0)  # Simula contagem de pacotes com erro
        ax.bar(['Pacotes com Erro'], [error_packets], color='red')
        ax.set_title("Contagem de Pacotes com Erro")
        ax.set_ylabel("Número de Pacotes com Erro")
        ax.set_ylim(0, error_packets + 10)  # Ajusta o limite do eixo Y
        # Formatar os eixos para mostrar apenas inteiros
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
        self.canvas_error_packets.draw()

# Função principal para capturar pacotes
def capture_packets(packet_count):
    print(f"\033[1mCapturando {packet_count} pacotes de forma contínua...")
    while True:
        if capturing:  # Captura pacotes apenas se a flag estiver ativa
            sniff(prn=packet_callback, count=packet_count)

# Função principal do programa
#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    window = App()
#    window.show()  # Exibir a janela
#    sys.exit(app.exec_())

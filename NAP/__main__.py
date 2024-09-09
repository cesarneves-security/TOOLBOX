import tkinter as tk
from tkinter import scrolledtext
import requests
import socket
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import time
from datetime import date

def show_url_info(url):
    try:
        response = requests.get(url)
        new_window = tk.Toplevel(root)
        new_window.title("Detalhes da URL")
        
        # Função para exibir cada bloco de informações com título
        def add_info_block(title, details):
            result_text.insert(tk.END, f"{title}:\n")
            for key, value in details.items():
                result_text.insert(tk.END, f" {key}: {value}\n")
            result_text.insert(tk.END, "\n")
        
        result_text = scrolledtext.ScrolledText(new_window, width=50, height=15, wrap=tk.WORD)
        result_text.pack(padx=10, pady=10)
        
        result_text.insert(tk.END, f"URL: {url}\n\n")
        result_text.insert(tk.END, "Detalhes:\n")

        # Bloco de informações
        headers_info = {
            "IP do Servidor": response.headers.get('Server', 'N/A'),
            "ID da Requisição": response.headers.get('X-Request-ID', 'N/A'),
            "Nome do Servidor": response.headers.get('Server', 'N/A'),
            "Nome do Sistema": response.headers.get('X-Powered-By', 'N/A'),
            "Cookies": response.cookies.get_dict(),
            "Sessão Atual": response.headers.get('Session', 'N/A'),
            "HTTP Server": response.headers.get('HTTP-Server', 'N/A'),
            "Versão do Server": response.headers.get('Server-Version', 'N/A'),
            "Versão do Sistema": response.headers.get('System-Version', 'N/A')
        }
        add_info_block("Informações Importantes", headers_info)
        
    except requests.exceptions.RequestException as e:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Erro ao tentar acessar a URL.")

def scan_url():
    url = url_entry.get()
    show_url_info(url)
    scan_ports(url)

def scan_ports(url):
    new_window = tk.Toplevel(root)
    new_window.title("Portas Abertas")
    
    result_text = scrolledtext.ScrolledText(new_window, width=50, height=15, wrap=tk.WORD)
    result_text.pack(padx=10, pady=10)
    
    with ThreadPoolExecutor() as executor:
        future = executor.submit(socket.gethostbyname, url)
        ip = future.result()
    
    for port in range(1, 1025):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            result = s.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                    result_text.insert(tk.END, f"Porta {port}: {service}\n")
                except OSError:
                    result_text.insert(tk.END, f"Porta {port}: Serviço desconhecido\n")

# Configuração da janela principal
root = tk.Tk()
root.title("Network Analyzer Pro")
root.geometry("400x400")

# Título
title_label = tk.Label(root, text="Network Analyzer", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Entrada de URL
url_label = tk.Label(root, text="URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=30)
url_entry.pack(pady=5)

# Botão para iniciar a análise da URL
scan_url_button = tk.Button(root, text="Scan URL", command=scan_url, bg="green", fg="white", padx=20, pady=10)
scan_url_button.pack(pady=10)

root.mainloop()
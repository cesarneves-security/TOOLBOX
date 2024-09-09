import socket

# Configurações do servidor
host = '192.168.18.11'  # Ou use o IP específico
port = 80

# Cria um socket e inicia o servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print(f"Servidor ouvindo em {host}:{port}...")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conexão recebida de {addr}")
            conn.sendall(b"Bem-vindo ao servidor!")

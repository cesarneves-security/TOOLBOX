import os
import sys
import pyperclip  # Para copiar a chave para a área de transferência
from cryptography.fernet import Fernet
from PyQt5 import QtWidgets

# Função para gerar uma chave
def generate_key():
    return Fernet.generate_key()

# Função para criptografar um arquivo
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as file:
        file.write(encrypted)

# Função para decriptografar um arquivo
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    try:
        with open(file_path, 'rb') as file:
            encrypted = file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(file_path, 'wb') as file:
            file.write(decrypted)
    except Exception as e:
        return f"Erro ao decriptografar {file_path}: {e}"

# Função para criptografar os nomes dos arquivos
def encrypt_file_name(file_name, key):
    fernet = Fernet(key)
    encrypted_name = fernet.encrypt(file_name.encode()).decode()
    return encrypted_name

# Função para criptografar todos os arquivos em um diretório
def encrypt_directory(directory, key):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            encrypted_name = encrypt_file_name(filename, key)
            os.rename(file_path, os.path.join(directory, encrypted_name))
            encrypt_file(os.path.join(directory, encrypted_name), key)

# Função para decriptografar todos os arquivos em um diretório
def decrypt_directory(directory, key):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            decrypt_file(file_path, key)
            decrypted_name = Fernet(key).decrypt(filename.encode()).decode()
            os.rename(file_path, os.path.join(directory, decrypted_name))

# Classe da Interface Gráfica
class CryptoApp(QtWidgets.QWidget):
    def __init__(self):
        super(CryptoApp, self).__init__()
        self.initUI()
        self.key = None  # Armazenar a chave gerada

    def initUI(self):
        self.setWindowTitle('Crypto App')
        self.setGeometry(100, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        # Entrada de caminho
        self.path_input = QtWidgets.QLineEdit(self)
        self.path_input.setPlaceholderText('Digite o caminho do arquivo ou diretório')
        layout.addWidget(self.path_input)

        # Entrada de chave (apenas para decriptografia)
        self.key_input = QtWidgets.QLineEdit(self)
        self.key_input.setPlaceholderText('Digite a chave (apenas para decriptografar)')
        layout.addWidget(self.key_input)

        # Botões
        self.encrypt_button = QtWidgets.QPushButton('Criptografar', self)
        self.copy_key_button = QtWidgets.QPushButton('Copiar Chave', self)
        self.decrypt_button = QtWidgets.QPushButton('Decriptografar', self)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.copy_key_button)
        layout.addWidget(self.decrypt_button)

        # Conectar os botões às funções
        self.encrypt_button.clicked.connect(self.encrypt_files)
        self.copy_key_button.clicked.connect(self.copy_key)
        self.decrypt_button.clicked.connect(self.decrypt_files)

        # Status
        self.status_label = QtWidgets.QLabel('', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def encrypt_files(self):
        path = self.path_input.text()
        self.key = generate_key()  # Gerar uma nova chave
        if os.path.isdir(path):
            encrypt_directory(path, self.key)
            self.status_label.setText(f"Diretório criptografado com a chave: {self.key.decode()}")
        else:
            encrypted_name = encrypt_file_name(os.path.basename(path), self.key)
            os.rename(path, os.path.join(os.path.dirname(path), encrypted_name))
            encrypt_file(path, self.key)
            self.status_label.setText(f"Arquivo criptografado com a chave: {self.key.decode()}")

    def copy_key(self):
        if self.key:
            pyperclip.copy(self.key.decode())
            self.status_label.setText("Chave copiada para a área de transferência.")
        else:
            self.status_label.setText("Nenhuma chave gerada para copiar.")

    def decrypt_files(self):
        path = self.path_input.text()
        key_input = self.key_input.text().encode()  # Converter a chave de string para bytes
        if os.path.isdir(path):
            decrypt_directory(path, key_input)
            self.status_label.setText("Diretório decriptografado com sucesso.")
        else:
            try:
                decrypt_file(path, key_input)
                decrypted_name = Fernet(key_input).decrypt(os.path.basename(path).encode()).decode()
                os.rename(path, os.path.join(os.path.dirname(path), decrypted_name))
                self.status_label.setText("Arquivo decriptografado com sucesso.")
            except Exception as e:
                self.status_label.setText(f"Erro na decriptação: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec_())

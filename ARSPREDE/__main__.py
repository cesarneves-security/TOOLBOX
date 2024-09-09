#***Nome: César Neves***
#importando as Bibliotecas Necessárias
import subprocess
import sys

# Lista de bibliotecas necessárias
required_packages = [
    'scapy',
    'pandas',
    'matplotlib',
    'PyQt5',
    'collections',
    'threading',
    'time',
    'sys'
]

def install(package):
    """Instala um pacote usando pip."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def check_and_install_packages():
    """Verifica se os pacotes estão instalados, e instala os que faltam."""
    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} \33[1mJá está instalado.")
        except ImportError:
            print(f"{package} \33[1m\33[91mNão está instalado. \33[93mInstalando...\33[0m")
            install(package)
            print(f"{package} \33[1m\33[93mInstalado com sucesso.\33[0m")

if __name__ == "__main__":
    check_and_install_packages()
    # Após a verificação e instalação, você pode executar o código principal
    from __arsp__ import * #importando o código principal
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = App()
        window.show()  # Exibir a janela
        sys.exit(app.exec_())

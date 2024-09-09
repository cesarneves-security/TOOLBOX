from __criptoware__ import *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    simulator = RansomwareSimulator()
    simulator.showFullScreen()
    sys.exit(app.exec_())

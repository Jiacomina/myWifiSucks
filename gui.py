import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QSpinBox, QPushButton
from PyQt5.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Why does my WiFi Suck?")
        self.setGeometry(50,50,500,300)
        self.setMinimumSize(QSize(500, 300))    
        self.setWindowIcon(QtGui.QIcon("no_wifi.png"))
        
        self.nodes_label = QLabel(self)
        self.nodes_label.resize(140,32)
        self.nodes_label.setText('Number of Nodes:')
        self.nodes_line = QSpinBox(self)
        self.nodes_line.move(160, 20)
        self.nodes_line.resize(200, 32)
        self.nodes_label.move(20, 20)

        self.range_label = QLabel(self)
        self.range_label.resize(140,32)
        self.range_label.setText('Range of Nodes (cm)')
        self.range_label.move(20, 60)
        self.range_line = QSpinBox(self)
        self.range_line.move(160, 60)
        self.range_line.resize(200, 32)

        file_button = QPushButton('Upload JSON File', self)
        file_button.clicked.connect(self.openFile)
        file_button.resize(140,32)
        file_button.move(20, 100)
        file_label = QLabel(self)
        file_label.setText('no file')
        file_label.move(160, 100)
        file_label.resize(200, 32)


        pybutton = QPushButton('OK', self)
        pybutton.resize(50,32)
        pybutton.move(20, 140) 

    def clickMethod(self):
        print('No.Nodes: ' + self.nodes_line.text() + ' Range: '+ self.range_line.text())

    def openFile(self):
        print("opening File")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()

    stylesheet = "QMainWindow{background-color: white}"

    app.setStyleSheet(stylesheet)  
    mainWin.show()
    sys.exit( app.exec_() )


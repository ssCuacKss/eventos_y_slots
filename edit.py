from os import listdir
from os.path import isfile, join
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QApplication, QLabel, QLineEdit, QTextEdit, QListWidget,QFileDialog)
from PyQt5.QtGui import QIcon

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        carpetaButton = QPushButton("Seleccionar")
        abrirButton = QPushButton("Abrir")
        guardarlButton = QPushButton("Guardar")
        gComoButton = QPushButton("Guardar como")
        CerrarButton = QPushButton("Cerrar")
        salirBUtton = QPushButton("Salir")

        carpetaButton.clicked.connect(self.rutadialog)
        salirBUtton.clicked.connect(self.close)
        CerrarButton.clicked.connect(self.limpiar)
        abrirButton.clicked.connect(self.abrir)
        guardarlButton.clicked.connect(self.guardar)
        gComoButton.clicked.connect(self.gcomo)

        self.label = QLabel("Carpeta:",self)
        self.label.move(10,15)

        self.carpetaTexto = QLineEdit(self)
        self.ficherosTexto = QListWidget(self)
        self.textoFichero = QTextEdit(self)
        
        self.carpetaTexto.move(70,15)
        self.carpetaTexto.resize(550,32)
        self.carpetaTexto.setStyleSheet("border: 1px solid #E3E4E5")
        self.carpetaTexto.setReadOnly(True)
        
        self.ficherosTexto.move(10,55)
        self.ficherosTexto.resize(200,380)
        self.ficherosTexto.setStyleSheet("border: 1px solid #E3E4E5")
        
        self.textoFichero.move(240,55)
        self.textoFichero.resize(380,380)
        self.textoFichero.setStyleSheet("border: 1px solid #E3E4E5")

        vbox = QVBoxLayout()
        vbox.addWidget(carpetaButton)
        vbox.addWidget(abrirButton)
        vbox.addWidget(guardarlButton)
        vbox.addWidget(gComoButton)
        vbox.addWidget(CerrarButton)
        vbox.addWidget(salirBUtton)

        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(vbox)

        self.setLayout(hbox)
        self.setWindowIcon(QIcon('web.png'))

        self.setGeometry(300, 300, 750, 450)
        self.setWindowTitle('Editor de texto')
        self.show()
    
    def rutadialog(self):
        dial = QFileDialog(self)
        dial.setWindowTitle('Elige una carpeta')
        dial.setFileMode(QFileDialog.Directory)
        dial.setDirectory("/home")
        val=dial.exec_()

        if val:

            self.ficherosTexto.clear()
            dir = dial.selectedFiles()
            self.commmonDir=dir[0]
            self.carpetaTexto.setText(dir[0])
            onlyfiles = [f for f in listdir(dir[0]) if isfile(join(dir[0], f))]

            for file in onlyfiles:
                self.ficherosTexto.addItem(file)
                self.ficherosTexto.itemClicked.connect(self.ClickedOp)

    def ClickedOp(self, item):
        self.filename = item.text()
    
    def limpiar(self):
        self.textoFichero.clear()

    def abrir(self):
        self.pressedDir = self.commmonDir+"/"+self.filename
        self.workingFile = self.pressedDir
        f = open(self.workingFile, 'r')
        with f:
            data = f.read()
            self.textoFichero.clear()
            self.textoFichero.setText(data)
            f.close()
    
    def guardar(self):
            if self.carpetaTexto.text() != "":
                f = open(self.workingFile, 'w')
                with f:
                    data = self.textoFichero.toPlainText()
                    f.write(data)
                    f.close()
            else:
                self.gcomo()

    def gcomo(self):
                dial = QFileDialog.getSaveFileName(self, "Guardar como")
                fname =dial[0]
                f = open(fname,"w")
                with f:
                    data = self.textoFichero.toPlainText()
                    f.write(data)
                    f.close()
                
                if self.commmonDir in fname:
                    onlyfiles = [f for f in listdir(self.commmonDir) if isfile(join(self.commmonDir, f))]
                    self.ficherosTexto.clear()
                    for file in onlyfiles:
                        self.ficherosTexto.addItem(file)
                        self.ficherosTexto.itemClicked.connect(self.ClickedOp)
                        


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

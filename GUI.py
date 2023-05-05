# -*- coding: utf-8 -*-
"""
Created on Thu May  4 19:50:47 2023

@author: juman
"""
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from client3 import Llamada
import threading
import time


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        # Crear los elementos de la interfaz
        self.labelDireccionIP = QLabel("Dirección IP de destino:")
        self.lineEditDireccionIP = QLineEdit()
        #self.lineEditDireccionIP.setInputMask("000.000.000.000;_")
        self.botonLlamar = QPushButton("Llamar")
        self.botonLlamar.clicked.connect(self.iniciar_llamada)

        # Crear un layout vertical y agregar los elementos
        layoutVertical = QVBoxLayout()
        layoutVertical.addWidget(self.labelDireccionIP)
        layoutVertical.addWidget(self.lineEditDireccionIP)
        layoutVertical.addWidget(self.botonLlamar)

        # Establecer el layout de la ventana principal
        self.setLayout(layoutVertical)
        self.setWindowTitle("Llamada VoIP")

    def iniciar_llamada(self):
        global llamada
        global hiloLlamada
        # Crear un objeto Llamada con la dirección IP especificada
        if(self.botonLlamar.text()=="Llamar"):
            #global llamada
            print("Here")
            self.botonLlamar.setText("Colgar")
            
            ipDestino = self.lineEditDireccionIP.text()
            llamada = Llamada(ipDestino)
    
            # Crear un hilo para la llamada y ejecutarlo
            hiloLlamada = threading.Thread(target=llamada.run)
            hiloLlamada.start()
            
            hiloChecarLlamada = threading.Thread(target=self.checarHiloLlamada)
            hiloChecarLlamada.start()
            
        elif(self.botonLlamar.text()=="Colgar"):
            #global llamada
            llamada.llamando = False
            time.sleep(1)
            self.botonLlamar.setText("Llamar")
    
    def checarHiloLlamada(self):
        global hiloLlamada
        while(self.botonLlamar.text()=="Colgar"):
            if(not hiloLlamada.is_alive()):
                self.botonLlamar.setText("Llamar")
            
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

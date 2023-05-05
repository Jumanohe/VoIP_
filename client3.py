# -*- coding: utf-8 -*-
"""
Created on Thu May  4 18:55:56 2023

@author: juman
"""
import socket
import pyaudio
import threading
import time

class Llamada():
    def __init__(self, ipDestino):
        self.ipDestino = ipDestino
        self.llamando = True
        # Configurar el socket UDP de escucha para recibir el audio:
        self.sockEscucha = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockEscucha.bind(('0.0.0.0', 8001))
        self.sockEscucha.settimeout(20)
        
        # configurar el audio de salida (bocinas)
        self.audioOutput = pyaudio.PyAudio()
        self.streamOutput = self.audioOutput.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
                
        # configurar el socket UDP de salida para mandar el audio
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
        # configurar el audio de entrada (micófono)
        self.audioInput = pyaudio.PyAudio()
        self.streamInput = self.audioInput.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True)
        
    # función para recibir y reproducir audio
    def recibir_audio(self):
        while self.llamando:
            try:
                data, addr = self.sockEscucha.recvfrom(2048)
                self.streamOutput.write(data)
            except socket.timeout:
                print("No se ha recibido nada en 10 segundos. Terminando el programa...")
                self.llamando = False
                
    # función para enviar audio en un hilo separado
    def enviar_audio(self):
        while self.llamando:
            data = self.streamInput.read(1024)
            self.sock1.sendto(data, (self.ipDestino, 8001))
    
    def run(self):
        # crear y ejecutar el hilo para recibir audio
        hilo_recibir = threading.Thread(target=self.recibir_audio)
        hilo_recibir.start()

        # crear y ejecutar el hilo para enviar audio
        hilo_enviar = threading.Thread(target=self.enviar_audio)
        hilo_enviar.start()

        # esperar a que termine el hilo de recibir antes de cerrar el socket y el audio
        hilo_recibir.join()
        time.sleep(1)
        self.sock1.close()
        self.sockEscucha.close()
        self.audioInput.terminate()
        self.audioOutput.terminate()
        
        
if __name__ == '__main__':
    ipDestino = '1.2.3.4'
    llamada = Llamada(ipDestino)
    hiloLlamada = threading.Thread(target=llamada.run)
    hiloLlamada.start()
    llamada.llamando= False

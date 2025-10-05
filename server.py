"""
Servidor TCP simples para cálculo de IMC (BMI Calculator).
Recebe peso e altura do cliente e retorna o resultado.
"""
import socket
import threading

def handle_client(client_socket, addr):
    print(f"Conexão de {addr}")
    try:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            return
        
        weight, height = map(float, data.split(','))
        bmi = weight / (height ** 2)

        if bmi < 18.5:
            result = "Thin"
        elif bmi < 25:
            result = "Normal"
        elif bmi < 30:
            result = "Overweight"
        else:
            result = "Fat"

        client_socket.send(f"BMI: {bmi:.2f} ({result})".encode('utf-8'))
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        client_socket.close()

def run_server():
    host = "0.0.0.0"
    port = 8000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Servidor ouvindo em {host}:{port}")

    try:
        while True:
            client_socket, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.close()

if __name__ == "__main__":
    run_server()

"""
Servidor TCP para cálculo de IMC (BMI Calculator).
Recebe peso e altura do cliente e retorna o resultado.
Melhorias:
- Reutilização de endereço (SO_REUSEADDR)
- Timeout de leitura
- Uso de sendall (garante envio completo)
- Threads daemon (encerra com o programa)
- Backlog configurado
"""

import socket
import threading

HOST = "0.0.0.0"
PORT = 8000
BACKLOG = 20
RECV_SIZE = 1024
TIMEOUT = 100


def handle_client(conn: socket.socket, addr):
    peer = f"{addr[0]}:{addr[1]}"
    print(f"Conexão recebida de {peer}")
    try:
        conn.settimeout(TIMEOUT)

        data = conn.recv(RECV_SIZE)
        if not data:
            print(f"[{peer}] Nenhum dado recebido.")
            return

        text = data.decode("utf-8").strip()
        weight, height = map(float, text.split(","))
        bmi = weight / (height ** 2)

        if bmi < 18.5:
            result = "Thin"
        elif bmi < 25:
            result = "Normal"
        elif bmi < 30:
            result = "Overweight"
        else:
            result = "Fat"

        message = f"BMI: {bmi:.2f} ({result})"
        conn.sendall(message.encode("utf-8"))

        print(f"[{peer}] peso={weight} altura={height} => {message}")

    except socket.timeout:
        print(f"[{peer}] Timeout de leitura.")
    except Exception as e:
        print(f"[{peer}] Erro: {e}")
    finally:
        conn.close()
        print(f"[{peer}] Conexão encerrada.")


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(BACKLOG)

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        try:
            while True:
                conn, addr = server.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    run_server()

import socket

def run_client():
    host = input("Digite o IP do servidor (ex: 127.0.0.1): ").strip()
    port = 8000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("Conectado ao servidor.\n")

    try:
        weight = float(input("Digite seu peso (kg): "))
        height = float(input("Digite sua altura (m): "))

        msg = f"{weight},{height}"
        client.send(msg.encode('utf-8'))

        result = client.recv(1024).decode('utf-8')
        print("Resultado:", result)
    except Exception as e:
        print("Erro:", e)
    finally:
        client.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    run_client()

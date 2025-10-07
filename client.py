"""
Cliente TCP para cálculo de IMC (BMI Calculator).
Melhorias:
- Uso de 'with' (fecha o socket automaticamente)
- Timeout de conexão e leitura
- Uso de sendall (garante envio completo)
- Tratamento de erros mais robusto
- Conversão de vírgula para ponto na entrada
"""

import socket

HOST_DEFAULT = "127.0.0.1"
PORT = 8000
TIMEOUT = 100
BUFFER_SIZE = 1024


def run_client():
    host = input(f"Digite o IP do servidor (padrão {HOST_DEFAULT}): ").strip() or HOST_DEFAULT

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(TIMEOUT)
            client.connect((host, PORT))
            print(f"Conectado ao servidor {host}:{PORT}\n")

            weight_str = input("Digite seu peso (kg): ").replace(",", ".").strip()
            height_str = input("Digite sua altura (m): ").replace(",", ".").strip()

            msg = f"{weight_str},{height_str}"
            client.sendall(msg.encode("utf-8"))

            response = client.recv(BUFFER_SIZE).decode("utf-8", errors="replace")
            print("Resultado:", response)

    except socket.timeout:
        print("Erro: Timeout de conexão ou leitura.")
    except ConnectionRefusedError:
        print("Erro: Servidor recusou a conexão. Verifique se ele está ativo.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        print("Conexão encerrada.")


if __name__ == "__main__":
    run_client()

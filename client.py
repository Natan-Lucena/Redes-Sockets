"""
Cliente TCP para IMC.
- Lê IP do servidor e envia "peso,altura".
- Mostra a resposta do servidor (Fat/Thin ou mensagem de erro).
"""
import socket

DEF_PORT = 55060  

def leia_float(prompt: str) -> float:
    while True:
        try:
            s = input(prompt).strip()
            s = s.replace(",", ".")
            return float(s)
        except ValueError:
            print("Valor inválido. Tente novamente.")


def run_client():
    host = input("Digite o IP do servidor (ex: 192.168.0.10): ").strip()
    port = DEF_PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(10)
        client.connect((host, port))
        print("Conectado ao servidor.\n")
        try:
            weight = leia_float("Digite seu peso (kg): ")
            height = leia_float("Digite sua altura (m, ex: 1.96 ou 196 para cm): ")
            payload = f"{weight},{height}"
            client.sendall(payload.encode("utf-8"))
            resp = client.recv(1024).decode("utf-8", errors="replace")
            print("Resultado:", resp)
        except socket.timeout:
            print("Erro: Timeout ao aguardar resposta do servidor.")

if __name__ == "__main__":
    run_client()
"""
Servidor TCP para cálculo de IMC (BMI Calculator) – versão alinhada ao enunciado.
- Protocolo: TCP (stream), cliente envia "peso,altura" em texto UTF-8.
- Servidor processa e responde APENAS "Gordo" ou "Magro" (em português).
- Suporta múltiplos clientes via threads.
- Valida entrada e converte altura em cm -> m quando apropriado.
"""
import socket
import threading

HOST = "0.0.0.0"
PORT = 55060  
BACKLOG = 50
RECV_BUFSIZE = 1024

# Função que classifica o BMI em português
def classifica_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "Abaixo do peso"
    elif bmi < 25:
        return "Peso normal"
    elif bmi < 30:
        return "Sobrepeso"
    elif bmi < 35:
        return "Obesidade grau 1"
    elif bmi < 40:
        return "Obesidade grau 2"
    else:
        return "Obesidade grau 3"

def parse_payload(data: str) -> tuple[float, float]:
    try:
        weight_str, height_str = data.split(",", 1)
        weight = float(weight_str.replace(",", ".").strip())
        height = float(height_str.replace(",", ".").strip())
        return weight, height
    except Exception as exc:
        raise ValueError("payload inválido, esperado 'peso,altura'") from exc

def normaliza_medidas(weight: float, height: float) -> tuple[float, float]:
    if height > 10:
        height = height / 100.0
    if weight <= 0 or height <= 0:
        raise ValueError("valores devem ser positivos")   
    if not (0 < weight <= 500 and 0 < height <= 3):
        raise ValueError("valores fora do intervalo razoável")
    return weight, height

def handle_client(conn: socket.socket, addr):
    peer = f"{addr[0]}:{addr[1]}"
    try:
        conn.settimeout(15)
        data = conn.recv(RECV_BUFSIZE)
        if not data:
            return
        text = data.decode("utf-8", errors="replace").strip()
        weight, height = parse_payload(text)
        weight, height = normaliza_medidas(weight, height)
        bmi = weight / (height * height)
        result = classifica_bmi(bmi)
        conn.sendall(result.encode("utf-8"))
        print(f"[{peer}] peso={weight:.2f}kg altura={height:.2f}m bmi={bmi:.2f} => {result}")
    except ValueError as ve:
        msg = f"Erro: {str(ve)}"
        try:
            conn.sendall(msg.encode("utf-8"))
        except Exception:
            pass
        print(f"[{peer}] {msg}")
    except socket.timeout:
        print(f"[{peer}] timeout de leitura")
    except Exception as e:
        print(f"[{peer}] Erro inesperado: {e}")
    finally:
        conn.close()

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(BACKLOG)
        print(f"Servidor ouvindo em {HOST}:{PORT}")
        try:
            while True:
                conn, addr = server.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")

if __name__ == "__main__":
    run_server()

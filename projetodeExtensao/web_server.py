from flask import Flask, send_from_directory
import threading
import os
from detector_colisao import DetectorColisao  # importa tua classe

app = Flask(__name__, static_folder="web/assets", static_url_path="/assets")

# === Rotas da interface ===
@app.route('/')
def serve_index():
    return send_from_directory('web', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

# === Função para rodar o detector em paralelo ===
def start_detector():
    detector = DetectorColisao()
    detector.run()

if __name__ == '__main__':
    # Roda o detector em uma thread separada
    threading.Thread(target=start_detector, daemon=True).start()

    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=5000)

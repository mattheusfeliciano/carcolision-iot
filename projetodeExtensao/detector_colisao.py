import os
import json
import time
import threading
import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

import paho.mqtt.client as mqtt
from colorama import Fore, Style, init

from config import MQTT_CONFIG, CONNECTION_CONFIG, LOGGING_CONFIG, DATA_CONFIG, UI_CONFIG, STATS_CONFIG

init(autoreset=True)


class DetectorColisao:
    """Sistema de Detecção de Colisão com MQTT, logging e persistência."""

    def __init__(self):
        # Diretórios base (ótimo para Docker)
        self.base_dir = Path(__file__).resolve().parent
        self.log_dir = self.base_dir / "logs"
        self.data_dir = self.base_dir / "data"
        self.log_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)

        # Carregar configurações
        self.mqtt_config = MQTT_CONFIG.copy()
        self.conn_config = CONNECTION_CONFIG.copy()
        self.log_config = LOGGING_CONFIG.copy()
        self.data_config = DATA_CONFIG.copy()
        self.ui_config = UI_CONFIG.copy()
        self.stats_config = STATS_CONFIG.copy()

        # Substitui host/paths por variáveis de ambiente (para Docker)
        self.mqtt_config["broker"] = os.getenv("MQTT_BROKER", self.mqtt_config["broker"])
        self.mqtt_config["port"] = int(os.getenv("MQTT_PORT", self.mqtt_config["port"]))
        self.data_config["data_file"] = os.getenv("DATA_FILE", str(self.data_dir / self.data_config["data_file"]))
        self.log_config["file"] = os.getenv("LOG_FILE", str(self.log_dir / self.log_config["file"]))

        # Inicializações
        self.reconnect_attempts = 0
        self.colisoes = []
        self.ultimo_evento = None
        self.conectado = False
        self._stop_event = threading.Event()

        self._setup_logging()
        self._setup_mqtt()
        self._start_auto_save()

    # ========== CONFIGURAÇÕES ==========
    def _setup_logging(self):
        """Configura logging rotativo com saída para arquivo e console."""
        logger = logging.getLogger("detector_colisao")
        logger.setLevel(getattr(logging, self.log_config["level"]))
        formatter = logging.Formatter(self.log_config["format"])

        # File Handler
        file_handler = RotatingFileHandler(
            self.log_config["file"],
            maxBytes=self.log_config["max_size"],
            backupCount=self.log_config["backup_count"],
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console Handler
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        logger.addHandler(console)

        self.logger = logger

    def _setup_mqtt(self):
        """Configura cliente MQTT e callbacks."""
        self.client = mqtt.Client(client_id=self.mqtt_config["client_id"], clean_session=self.mqtt_config["clean_session"])
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        if self.mqtt_config["username"]:
            self.client.username_pw_set(self.mqtt_config["username"], self.mqtt_config["password"])

    # ========== CALLBACKS MQTT ==========
    def _on_connect(self, client, userdata, flags, rc):
        """Callback executado ao conectar no broker."""
        if rc == 0:
            self.conectado = True
            self.reconnect_attempts = 0
            self._print("✅ Conectado ao broker MQTT!", Fore.GREEN)
            self.client.subscribe(self.mqtt_config["topic"], qos=self.mqtt_config["qos"])
        else:
            self._print(f"⚠️ Falha na conexão. Código: {rc}", Fore.YELLOW)
            self._attempt_reconnect()

    def _on_disconnect(self, client, userdata, rc):
        """Callback executado ao perder a conexão."""
        self.conectado = False
        self._print("⚠️ Desconectado do broker MQTT!", Fore.RED)
        self._attempt_reconnect()

    def _on_message(self, client, userdata, msg):
        """Callback executado ao receber mensagem."""
        try:
            payload = msg.payload.decode("utf-8")
            data = json.loads(payload)
            timestamp = datetime.now().strftime(self.ui_config["date_format"])
            registro = {"timestamp": timestamp, "dados": data}
            self.colisoes.append(registro)
            self.ultimo_evento = timestamp
            self._print(f"💥 Colisão detectada em {timestamp}", Fore.CYAN)
        except Exception as e:
            self.logger.error(f"Erro ao processar mensagem: {e}")

    # ========== RECONEXÃO ==========
    def _attempt_reconnect(self):
        """Tenta reconectar de forma não bloqueante."""
        if self.reconnect_attempts >= self.conn_config["max_reconnect_attempts"]:
            self._print("❌ Máximo de tentativas de reconexão atingido.", Fore.RED)
            return

        self.reconnect_attempts += 1
        delay = self.conn_config["reconnect_delay"] * self.reconnect_attempts
        self.logger.warning(f"Tentativa de reconexão {self.reconnect_attempts} em {delay}s")
        threading.Timer(delay, self._try_reconnect).start()

    def _try_reconnect(self):
        """Executa reconexão MQTT."""
        try:
            self.client.reconnect()
        except Exception as e:
            self.logger.error(f"Erro na reconexão: {e}")
            self._attempt_reconnect()

    # ========== AUTO SAVE ==========
    def _start_auto_save(self):
        """Thread de salvamento automático de dados."""
        def auto_save_worker():
            while not self._stop_event.wait(self.data_config["auto_save_interval"]):
                self._save_data()
        threading.Thread(target=auto_save_worker, daemon=True).start()

    def _save_data(self):
        """Salva histórico de colisões em arquivo JSON."""
        if not self.data_config["save_to_file"]:
            return
        try:
            with open(self.data_config["data_file"], "w", encoding="utf-8") as f:
                json.dump(self.colisoes[-self.data_config["max_history_size"]:], f, indent=4)
            self.logger.info("Histórico salvo com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao salvar histórico: {e}")

    # ========== IMPRESSÃO ==========
    def _print(self, msg="", color=Fore.WHITE, style=Style.NORMAL, sep=False, length=None):
        """Imprime mensagens padronizadas e coloridas."""
        if sep:
            char = self.ui_config["separator_char"]
            length = length or self.ui_config["separator_length"]
            msg = char * length
        if self.ui_config["use_colors"]:
            print(f"{style}{color}{msg}{Style.RESET_ALL}")
        else:
            print(msg)

    # ========== CICLO PRINCIPAL ==========
    def run(self):
        """Executa o detector continuamente."""
        try:
            self._print(sep=True)
            self._print("🚀 Iniciando Sistema de Detecção de Colisões", Fore.GREEN, Style.BRIGHT)
            self._print(sep=True)

            self.client.connect(
                self.mqtt_config["broker"],
                self.mqtt_config["port"],
                self.mqtt_config["keepalive"]
            )
            self.client.loop_start()

            while not self._stop_event.is_set():
                if self.conectado:
                    self._check_connection_health()
                time.sleep(1)

        except KeyboardInterrupt:
            self._print("\n🛑 Encerrando sistema...", Fore.YELLOW)
        finally:
            self._cleanup()

    def _check_connection_health(self):
        """Monitora taxa de colisões e emite alertas."""
        if not self.colisoes:
            return

        intervalo = 60  # segundos
        agora = datetime.now()
        recentes = [
            c for c in self.colisoes
            if (agora - datetime.strptime(c["timestamp"], self.ui_config["date_format"])).total_seconds() <= intervalo
        ]
        if len(recentes) > self.stats_config["alert_threshold"]:
            self._print("🚨 ALERTA: Alta taxa de colisões detectada!", Fore.RED, Style.BRIGHT)
            self.logger.warning("Alta taxa de colisões detectada.")

    def _cleanup(self):
        """Finaliza corretamente o sistema."""
        self._stop_event.set()
        self._save_data()
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info("Sistema finalizado com segurança.")


if __name__ == "__main__":
    DetectorColisao().run()

"""
Arquivo de configuração para o Sistema de Detecção de Colisão.
Modifique os valores conforme necessário para ajustar o comportamento do sistema.
"""

from pathlib import Path

# ===== CONFIGURAÇÕES MQTT =====
MQTT_CONFIG: dict = {
    "broker": "mosquitto",           # Endereço do broker MQTT (Docker/local)
    "port": 1883,
    "keepalive": 60,
    "username": None,                # Sem autenticação padrão
    "password": None,
    "client_id": "detector_colisao_pc",
    "topic": "vini123/colisao",
    "qos": 1,                        # Quality of Service: 0, 1 ou 2
    "retain": False,                 # Mantém a última mensagem no broker
    "clean_session": True
}

# ===== CONFIGURAÇÕES DE CONEXÃO =====
CONNECTION_CONFIG: dict = {
    "timeout": 10,                   # Tempo limite para conectar (segundos)
    "reconnect_delay": 5,            # Intervalo entre tentativas de reconexão
    "max_reconnect_attempts": 10,
    "ping_interval": 30              # Intervalo de envio de ping (segundos)
}

# ===== CONFIGURAÇÕES DE LOGGING =====
LOGGING_CONFIG: dict = {
    "level": "INFO",                 # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "file": Path("logs/colisao.log"),# Caminho do arquivo de log
    "max_size": 10 * 1024 * 1024,    # 10 MB
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# ===== CONFIGURAÇÕES DE PERSISTÊNCIA =====
DATA_CONFIG: dict = {
    "save_to_file": True,
    "data_file": Path("data/historico_colisoes.json"),
    "auto_save_interval": 30,        # Salvar automaticamente a cada X segundos
    "max_history_size": 1000         # Máximo de registros mantidos em memória
}

# ===== CONFIGURAÇÕES DE INTERFACE =====
UI_CONFIG: dict = {
    "show_timestamp": True,
    "show_topic": True,
    "show_message": True,
    "use_colors": True,
    "date_format": "%d/%m/%Y %H:%M:%S",
    "separator_char": "=",
    "separator_length": 60
}

# ===== CONFIGURAÇÕES DE ESTATÍSTICAS =====
STATS_CONFIG: dict = {
    "show_rate_per_minute": True,
    "show_rate_per_hour": True,
    "show_peak_hour": True,
    "show_average_interval": True,
    "alert_threshold": 10             # Alerta se houver mais de X colisões/min
}

# ===== AGRUPAMENTO GERAL (para facilitar importação) =====
CONFIG: dict = {
    "mqtt": MQTT_CONFIG,
    "connection": CONNECTION_CONFIG,
    "logging": LOGGING_CONFIG,
    "data": DATA_CONFIG,
    "ui": UI_CONFIG,
    "stats": STATS_CONFIG
}

"""
Arquivo de configuração para o Sistema de Detecção de Colisão
Modifique os valores aqui para ajustar o comportamento do sistema
"""

# ===== CONFIGURAÇÕES MQTT =====
MQTT_CONFIG = {
    "broker": "localhost",  # Broker local Docker
    "port": 1883,
    "keepalive": 60,
    "username": None,  # Sem autenticação para broker local
    "password": None,  # Deixe None se não usar autenticação
    "client_id": "detector_colisao_pc",
    "topic": "vini123/colisao",
    "qos": 1,  # Quality of Service: 0, 1 ou 2
    "retain": False,  # Se True, broker mantém última mensagem
    "clean_session": True
}

# ===== CONFIGURAÇÕES DE CONEXÃO =====
CONNECTION_CONFIG = {
    "timeout": 10,  # Tempo limite para conectar (segundos)
    "reconnect_delay": 5,  # Delay entre tentativas de reconexão
    "max_reconnect_attempts": 10,  # Máximo de tentativas de reconexão
    "ping_interval": 30  # Intervalo para ping (segundos)
}

# ===== CONFIGURAÇÕES DE LOGGING =====
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "file": "colisao.log",
    "max_size": 10485760,  # 10MB
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# ===== CONFIGURAÇÕES DE PERSISTÊNCIA =====
DATA_CONFIG = {
    "save_to_file": True,
    "data_file": "historico_colisoes.json",
    "auto_save_interval": 30,  # Salvar automaticamente a cada X segundos
    "max_history_size": 1000  # Máximo de registros em memória
}

# ===== CONFIGURAÇÕES DE INTERFACE =====
UI_CONFIG = {
    "show_timestamp": True,
    "show_topic": True,
    "show_message": True,
    "use_colors": True,
    "date_format": "%d/%m/%Y %H:%M:%S",
    "separator_char": "=",
    "separator_length": 60
}

# ===== CONFIGURAÇÕES DE ESTATÍSTICAS =====
STATS_CONFIG = {
    "show_rate_per_minute": True,
    "show_rate_per_hour": True,
    "show_peak_hour": True,
    "show_average_interval": True,
    "alert_threshold": 10  # Alerta se mais de X colisões por minuto
}

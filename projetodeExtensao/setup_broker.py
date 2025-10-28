#!/usr/bin/env python3
"""
Script de Setup do Broker MQTT
Configura e testa o broker MQTT para o projeto
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(command, description):
    """Executa comando e retorna resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso!")
            return True
        else:
            print(f"❌ {description} - Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False

def check_docker():
    """Verifica se Docker está instalado"""
    print("🔍 Verificando Docker...")
    result = subprocess.run("docker --version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Docker encontrado: {result.stdout.strip()}")
        return True
    else:
        print("❌ Docker não encontrado!")
        print("📥 Instale Docker Desktop: https://www.docker.com/products/docker-desktop")
        return False

def check_docker_compose():
    """Verifica se Docker Compose está disponível"""
    print("🔍 Verificando Docker Compose...")
    result = subprocess.run("docker-compose --version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Docker Compose encontrado: {result.stdout.strip()}")
        return True
    else:
        print("❌ Docker Compose não encontrado!")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("📁 Criando diretórios...")
    directories = ["data", "logs"]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Diretório '{dir_name}' criado")
    
    return True

def start_broker():
    """Inicia o broker MQTT"""
    print("🚀 Iniciando broker MQTT...")
    
    # Para containers existentes
    subprocess.run("docker-compose down", shell=True)
    
    # Inicia novos containers
    success = run_command("docker-compose up -d", "Iniciando containers")
    
    if success:
        print("⏳ Aguardando broker inicializar...")
        time.sleep(5)
        
        # Verifica se está rodando
        result = subprocess.run("docker-compose ps", shell=True, capture_output=True, text=True)
        print("📊 Status dos containers:")
        print(result.stdout)
        
        return True
    return False

def test_connection():
    """Testa conexão com o broker"""
    print("🧪 Testando conexão MQTT...")
    
    try:
        import paho.mqtt.client as mqtt
        
        client = mqtt.Client()
        connected = False
        
        def on_connect(client, userdata, flags, rc):
            nonlocal connected
            if rc == 0:
                connected = True
                print("✅ Conexão MQTT bem-sucedida!")
            else:
                print(f"❌ Erro de conexão: {rc}")
        
        client.on_connect = on_connect
        client.connect("localhost", 1883, 60)
        client.loop_start()
        
        # Aguarda conexão
        timeout = 10
        start_time = time.time()
        while not connected and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        client.loop_stop()
        client.disconnect()
        
        return connected
        
    except ImportError:
        print("❌ Biblioteca paho-mqtt não encontrada!")
        print("📥 Execute: pip install paho-mqtt")
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def update_config():
    """Atualiza configuração para usar broker local"""
    print("⚙️ Atualizando configuração...")
    
    config_content = '''# ===== CONFIGURAÇÕES MQTT =====
MQTT_CONFIG = {
    "broker": "localhost",  # Broker local
    "port": 1883,          # Porta TCP
    "keepalive": 60,
    "username": None,       # Sem autenticação
    "password": None,
    "client_id": "detector_colisao_pc",
    "topic": "vini123/colisao",
    "qos": 1,
    "retain": False,
    "clean_session": True
}

# ===== CONFIGURAÇÕES DE CONEXÃO =====
CONNECTION_CONFIG = {
    "timeout": 10,
    "reconnect_delay": 5,
    "max_reconnect_attempts": 10,
    "ping_interval": 30
}

# ===== CONFIGURAÇÕES DE LOGGING =====
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "colisao.log",
    "max_size": 10485760,  # 10MB
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# ===== CONFIGURAÇÕES DE PERSISTÊNCIA =====
DATA_CONFIG = {
    "save_to_file": True,
    "data_file": "historico_colisoes.json",
    "auto_save_interval": 30,
    "max_history_size": 1000
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
    "alert_threshold": 10
}'''
    
    try:
        with open("config.py", "w", encoding="utf-8") as f:
            f.write(config_content)
        print("✅ Configuração atualizada para broker local")
        return True
    except Exception as e:
        print(f"❌ Erro ao atualizar configuração: {e}")
        return False

def show_status():
    """Mostra status do sistema"""
    print("\n" + "=" * 60)
    print("📊 STATUS DO SISTEMA MQTT")
    print("=" * 60)
    
    # Status dos containers
    result = subprocess.run("docker-compose ps", shell=True, capture_output=True, text=True)
    print("🐳 Containers Docker:")
    print(result.stdout)
    
    # URLs de acesso
    print("🌐 URLs de Acesso:")
    print("  • MQTT TCP: localhost:1883")
    print("  • MQTT WebSocket: localhost:8081")
    print("  • MQTT Explorer: http://localhost:4000")
    
    print("\n📋 Próximos Passos:")
    print("  1. Execute: python detector_colisao.py")
    print("  2. Abra: detector-colisao.html")
    print("  3. Configure: localhost:8081 no HTML")
    print("  4. Teste a integração!")
    
    print("=" * 60)

def main():
    """Função principal"""
    print("\n" + "=" * 60)
    print("🚀 SETUP DO BROKER MQTT")
    print("=" * 60)
    
    # Verificações
    if not check_docker():
        return False
    
    if not check_docker_compose():
        return False
    
    # Setup
    if not create_directories():
        return False
    
    if not start_broker():
        return False
    
    if not test_connection():
        print("⚠️ Broker iniciado, mas teste de conexão falhou")
        print("💡 Tente novamente em alguns segundos")
    
    if not update_config():
        return False
    
    show_status()
    
    print("\n✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("🎯 Seu broker MQTT está rodando e pronto para uso!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup falhou. Verifique os erros acima.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante setup: {e}")
        sys.exit(1)






#!/usr/bin/env python3
"""
Teste Rápido do Sistema
Verifica se todos os componentes estão funcionando
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Testa imports necessários"""
    print("🔍 Testando imports...")
    
    try:
        import paho.mqtt.client as mqtt
        print("✅ paho-mqtt OK")
    except ImportError:
        print("❌ paho-mqtt não encontrado")
        return False
    
    try:
        from colorama import init, Fore, Style
        print("✅ colorama OK")
    except ImportError:
        print("❌ colorama não encontrado")
        return False
    
    try:
        from config import MQTT_CONFIG
        print("✅ config.py OK")
    except ImportError:
        print("❌ config.py não encontrado")
        return False
    
    return True

def test_files():
    """Testa arquivos necessários"""
    print("\n📁 Testando arquivos...")
    
    files = [
        "detector_colisao.py",
        "config.py", 
        "requirements.txt",
        "detector-colisao.html",
        "docker-compose.yml",
        "mosquitto.conf"
    ]
    
    all_ok = True
    for file in files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} não encontrado")
            all_ok = False
    
    return all_ok

def test_directories():
    """Testa diretórios"""
    print("\n📂 Testando diretórios...")
    
    # Cria diretórios se não existirem
    directories = ["logs", "data"]
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ {dir_name}/")
    
    return True

def show_next_steps():
    """Mostra próximos passos"""
    print("\n" + "=" * 60)
    print("🎯 PRÓXIMOS PASSOS PARA CONFIGURAR BROKER MQTT")
    print("=" * 60)
    
    print("\n📋 OPÇÃO 1: Docker (Recomendado)")
    print("  1. Instale Docker Desktop")
    print("  2. Execute: python setup_broker.py")
    print("  3. Aguarde containers iniciarem")
    print("  4. Teste: python detector_colisao.py")
    
    print("\n📋 OPÇÃO 2: Broker Público")
    print("  1. Use: mqtt.eclipseprojects.io:1883")
    print("  2. Execute: python detector_colisao.py")
    print("  3. Abra: detector-colisao.html")
    print("  4. Configure: mqtt.eclipseprojects.io:8081")
    
    print("\n📋 OPÇÃO 3: Mosquitto Local")
    print("  1. Instale Mosquitto")
    print("  2. Configure mosquitto.conf")
    print("  3. Execute: mosquitto -c mosquitto.conf")
    print("  4. Teste conexão")
    
    print("\n🔧 COMANDOS ÚTEIS:")
    print("  • Iniciar broker Docker: docker-compose up -d")
    print("  • Ver logs: docker-compose logs -f mosquitto")
    print("  • Parar broker: docker-compose down")
    print("  • Testar conexão: python teste_conectividade.py")
    
    print("\n📖 DOCUMENTAÇÃO:")
    print("  • Guia completo: GUIA_BROKER_MQTT.md")
    print("  • Relatório de teste: RELATORIO_TESTE_INTEGRACAO.md")
    
    print("=" * 60)

def main():
    """Função principal"""
    print("\n" + "=" * 60)
    print("🧪 TESTE RÁPIDO DO SISTEMA")
    print("=" * 60)
    
    # Testes
    imports_ok = test_imports()
    files_ok = test_files()
    dirs_ok = test_directories()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DOS TESTES")
    print("=" * 60)
    
    if imports_ok and files_ok and dirs_ok:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎉 Sistema pronto para configuração do broker MQTT")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("🔧 Corrija os problemas antes de continuar")
    
    show_next_steps()
    
    return imports_ok and files_ok and dirs_ok

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🚀 Pronto para configurar o broker MQTT!")
        else:
            print("\n⚠️ Corrija os problemas antes de continuar")
    except Exception as e:
        print(f"\n❌ Erro durante teste: {e}")






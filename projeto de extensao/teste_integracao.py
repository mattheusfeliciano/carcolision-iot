#!/usr/bin/env python3
"""
Script de Teste de Integração MQTT
Simula mensagens de colisão para testar a comunicação entre sistemas
"""

import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# Configurações MQTT
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = "vini123/colisao"
MQTT_USERNAME = "vini123"

class MQTTTester:
    def __init__(self):
        self.client = None
        self.connected = False
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("✅ Conectado ao broker MQTT com sucesso!")
            print(f"📡 Broker: {MQTT_BROKER}:{MQTT_PORT}")
            print(f"📝 Tópico: {MQTT_TOPIC}")
            print("=" * 50)
        else:
            print(f"❌ Erro ao conectar: {rc}")
            
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        print("⚠️ Desconectado do broker MQTT")
        
    def connect(self):
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="teste_integracao")
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            
            # Configura autenticação se necessário
            if MQTT_USERNAME:
                self.client.username_pw_set(MQTT_USERNAME, None)
                
            print(f"🔌 Conectando ao broker MQTT...")
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            
            # Aguarda conexão
            timeout = 10
            start_time = time.time()
            while not self.connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)
                
            return self.connected
            
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    
    def send_collision_message(self, collision_number, sensor_id="teste_sensor"):
        """Envia mensagem de colisão simulada"""
        if not self.connected:
            print("❌ Não conectado ao MQTT!")
            return False
            
        message = {
            "tipo": "colisao",
            "mensagem": f"Colisão #{collision_number} detectada pelo sensor {sensor_id}",
            "sensor_id": sensor_id,
            "timestamp": datetime.now().isoformat(),
            "distancia": round(random.uniform(5, 15), 1),
            "velocidade": round(random.uniform(30, 80), 1),
            "intensidade": random.choice(["baixa", "media", "alta"]),
            "localizacao": random.choice(["frontal", "lateral_esquerda", "lateral_direita", "traseira"])
        }
        
        try:
            json_message = json.dumps(message, ensure_ascii=False)
            result = self.client.publish(MQTT_TOPIC, json_message, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"✅ Colisão #{collision_number} enviada com sucesso!")
                print(f"   📝 Mensagem: {message['mensagem']}")
                print(f"   📊 Distância: {message['distancia']}cm")
                print(f"   🚗 Velocidade: {message['velocidade']}%")
                print(f"   📍 Localização: {message['localizacao']}")
                print("-" * 40)
                return True
            else:
                print(f"❌ Erro ao enviar mensagem: {result.rc}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            return False
    
    def send_status_message(self, status="sistema_ok"):
        """Envia mensagem de status"""
        if not self.connected:
            print("❌ Não conectado ao MQTT!")
            return False
            
        message = {
            "tipo": "status",
            "mensagem": f"Status do sistema: {status}",
            "sensor_id": "sistema_teste",
            "timestamp": datetime.now().isoformat(),
            "status": status
        }
        
        try:
            json_message = json.dumps(message, ensure_ascii=False)
            result = self.client.publish(MQTT_TOPIC, json_message, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"✅ Status enviado: {status}")
                return True
            else:
                print(f"❌ Erro ao enviar status: {result.rc}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar status: {e}")
            return False
    
    def run_test_sequence(self):
        """Executa sequência de testes"""
        print("\n" + "=" * 60)
        print("🧪 INICIANDO TESTE DE INTEGRAÇÃO MQTT")
        print("=" * 60)
        
        if not self.connect():
            print("❌ Falha na conexão. Teste abortado.")
            return
        
        print("\n📋 SEQUÊNCIA DE TESTES:")
        print("1. Enviando mensagem de status inicial...")
        self.send_status_message("sistema_iniciado")
        time.sleep(2)
        
        print("\n2. Simulando colisões...")
        for i in range(1, 6):
            print(f"\n🚗 Simulando colisão #{i}...")
            self.send_collision_message(i, f"sensor_{i}")
            time.sleep(3)  # Intervalo entre colisões
        
        print("\n3. Enviando mensagem de status final...")
        self.send_status_message("teste_concluido")
        time.sleep(2)
        
        print("\n" + "=" * 60)
        print("✅ TESTE DE INTEGRAÇÃO CONCLUÍDO!")
        print("=" * 60)
        print("📊 Verifique:")
        print("   • Sistema Python: logs em logs/colisao.log")
        print("   • Interface HTML: console de eventos")
        print("   • Arquivo de dados: historico_colisoes.json")
        print("=" * 60)
    
    def disconnect(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            print("🔌 Desconectado do broker MQTT")

def main():
    """Função principal do teste"""
    tester = MQTTTester()
    
    try:
        tester.run_test_sequence()
    except KeyboardInterrupt:
        print("\n\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
    finally:
        tester.disconnect()

if __name__ == "__main__":
    main()

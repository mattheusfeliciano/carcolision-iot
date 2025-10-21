#!/usr/bin/env python3
"""
Simulador de colisões para testar o sistema completo
"""

import paho.mqtt.client as mqtt
import time
import json
import random

def simulate_collisions():
    print("🚗 Simulador de Colisões IoT")
    print("=" * 50)
    
    # Configuração
    broker = "localhost"
    port = 1883
    topic = "vini123/colisao"
    
    try:
        # Criar cliente MQTT
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="simulador_colisoes")
        
        def on_connect(client, userdata, flags, rc, properties=None):
            if rc == 0:
                print("✅ Conectado ao broker local!")
                print(f"📡 Broker: {broker}:{port}")
                print(f"📝 Tópico: {topic}")
                print("\n🚗 Iniciando simulação de colisões...")
                print("Pressione Ctrl+C para parar\n")
            else:
                print(f"❌ Erro de conexão: {rc}")
        
        def on_publish(client, userdata, mid, reason_code, properties=None):
            print(f"📤 Mensagem #{mid} enviada!")
        
        client.on_connect = on_connect
        client.on_publish = on_publish
        
        # Conectar
        client.connect(broker, port, 60)
        client.loop_start()
        
        # Aguardar conexão
        time.sleep(2)
        
        # Simular colisões
        collision_count = 0
        
        while True:
            # Simular diferentes tipos de colisão
            collision_types = [
                "colisão frontal",
                "colisão lateral",
                "colisão traseira", 
                "colisão múltipla",
                "quase colisão"
            ]
            
            sensors = ["sensor_a", "sensor_b", "sensor_c", "sensor_d"]
            
            collision_count += 1
            
            # Criar mensagem de colisão
            collision_data = {
                "tipo": "colisao",
                "sensor": random.choice(sensors),
                "timestamp": time.time(),
                "colisao_id": collision_count,
                "tipo_colisao": random.choice(collision_types),
                "intensidade": random.randint(1, 10),
                "localizacao": {
                    "x": random.randint(0, 100),
                    "y": random.randint(0, 100)
                },
                "velocidade": random.randint(20, 120),
                "mensagem": f"Colisão #{collision_count} detectada no {random.choice(sensors)}"
            }
            
            # Publicar mensagem
            message = json.dumps(collision_data, indent=2)
            client.publish(topic, message, qos=1)
            
            print(f"🔴 Colisão #{collision_count}: {collision_data['tipo_colisao']} - {collision_data['sensor']}")
            print(f"   📍 Localização: ({collision_data['localizacao']['x']}, {collision_data['localizacao']['y']})")
            print(f"   🚗 Velocidade: {collision_data['velocidade']} km/h")
            print(f"   ⚡ Intensidade: {collision_data['intensidade']}/10")
            print("-" * 50)
            
            # Aguardar entre colisões (1-5 segundos)
            time.sleep(random.randint(1, 5))
            
    except KeyboardInterrupt:
        print("\n\n🛑 Simulação interrompida pelo usuário")
        print(f"📊 Total de colisões simuladas: {collision_count}")
        client.disconnect()
        print("✅ Desconectado do broker")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    simulate_collisions()



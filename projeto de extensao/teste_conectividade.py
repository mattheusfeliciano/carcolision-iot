#!/usr/bin/env python3
"""
Teste Simples de Conectividade MQTT
"""

import paho.mqtt.client as mqtt
import time

def test_mqtt_connection():
    print("🔌 Testando conectividade MQTT...")
    
    # Testa diferentes brokers e portas
    brokers = [
        ("mqtt.eclipseprojects.io", 1883),
        ("broker.hivemq.com", 1883),
        ("test.mosquitto.org", 1883),
        ("mqtt.eclipseprojects.io", 8081)
    ]
    
    for broker, port in brokers:
        print(f"\n📡 Testando {broker}:{port}...")
        
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="teste_conectividade")
            
            def on_connect(client, userdata, flags, rc, properties=None):
                if rc == 0:
                    print(f"✅ Conectado com sucesso!")
                    client.disconnect()
                else:
                    print(f"❌ Erro de conexão: {rc}")
            
            client.on_connect = on_connect
            client.connect(broker, port, 60)
            client.loop_start()
            
            # Aguarda conexão por 5 segundos
            time.sleep(5)
            client.loop_stop()
            client.disconnect()
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 50)
    print("🧪 Teste de conectividade concluído!")

if __name__ == "__main__":
    test_mqtt_connection()






#!/usr/bin/env python3
"""
Simulador Local de Integração MQTT
Demonstra como o sistema funcionaria com dados simulados
"""

import json
import time
import random
from datetime import datetime
from pathlib import Path

class SimuladorIntegracao:
    def __init__(self):
        self.colisoes_detectadas = 0
        self.historico = []
        self.log_file = Path("logs/simulacao.log")
        self.data_file = Path("historico_simulacao.json")
        
        # Cria diretório de logs
        self.log_file.parent.mkdir(exist_ok=True)
        
    def log_event(self, message, level="INFO"):
        """Registra evento no log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        print(f"📝 {log_entry.strip()}")
    
    def simular_colisao(self, sensor_id="simulador"):
        """Simula uma colisão"""
        self.colisoes_detectadas += 1
        timestamp = datetime.now()
        
        colisao = {
            'numero': self.colisoes_detectadas,
            'timestamp': timestamp.isoformat(),
            'mensagem': f'Colisão #{self.colisoes_detectadas} detectada pelo {sensor_id}',
            'sensor_id': sensor_id,
            'topic': 'vini123/colisao',
            'qos': 1,
            'distancia': round(random.uniform(5, 15), 1),
            'velocidade': round(random.uniform(30, 80), 1),
            'intensidade': random.choice(["baixa", "media", "alta"]),
            'localizacao': random.choice(["frontal", "lateral_esquerda", "lateral_direita", "traseira"])
        }
        
        self.historico.append(colisao)
        
        # Log da colisão
        self.log_event(f"COLISÃO DETECTADA #{self.colisoes_detectadas}")
        self.log_event(f"  📍 Localização: {colisao['localizacao']}")
        self.log_event(f"  📏 Distância: {colisao['distancia']}cm")
        self.log_event(f"  🚗 Velocidade: {colisao['velocidade']}%")
        self.log_event(f"  ⚡ Intensidade: {colisao['intensidade']}")
        
        return colisao
    
    def simular_mensagem_mqtt(self, colisao):
        """Simula envio de mensagem MQTT"""
        mensagem_mqtt = {
            "tipo": "colisao",
            "mensagem": colisao['mensagem'],
            "sensor_id": colisao['sensor_id'],
            "timestamp": colisao['timestamp'],
            "distancia": colisao['distancia'],
            "velocidade": colisao['velocidade'],
            "intensidade": colisao['intensidade'],
            "localizacao": colisao['localizacao']
        }
        
        json_message = json.dumps(mensagem_mqtt, ensure_ascii=False, indent=2)
        
        self.log_event("📡 MENSAGEM MQTT SIMULADA:")
        self.log_event(f"  Tópico: vini123/colisao")
        self.log_event(f"  QoS: 1")
        self.log_event(f"  Payload: {json_message}")
        
        return json_message
    
    def salvar_dados(self):
        """Salva dados da simulação"""
        dados = {
            'total_colisoes': self.colisoes_detectadas,
            'historico': self.historico,
            'last_save': datetime.now().isoformat(),
            'simulacao': True
        }
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        self.log_event("💾 Dados salvos em historico_simulacao.json")
    
    def exibir_estatisticas(self):
        """Exibe estatísticas da simulação"""
        print("\n" + "=" * 60)
        print("📊 ESTATÍSTICAS DA SIMULAÇÃO")
        print("=" * 60)
        print(f"Total de colisões: {self.colisoes_detectadas}")
        
        if self.historico:
            primeira = datetime.fromisoformat(self.historico[0]['timestamp'])
            ultima = datetime.fromisoformat(self.historico[-1]['timestamp'])
            duracao = (ultima - primeira).total_seconds()
            
            print(f"Primeira colisão: {primeira.strftime('%H:%M:%S')}")
            print(f"Última colisão: {ultima.strftime('%H:%M:%S')}")
            
            if duracao > 0:
                taxa = self.colisoes_detectadas / (duracao / 60)
                print(f"Taxa média: {taxa:.2f} colisões/minuto")
            
            # Análise por localização
            localizacoes = {}
            for colisao in self.historico:
                loc = colisao['localizacao']
                localizacoes[loc] = localizacoes.get(loc, 0) + 1
            
            print("\n📍 Colisões por localização:")
            for loc, count in sorted(localizacoes.items(), key=lambda x: x[1], reverse=True):
                print(f"  {loc}: {count} colisões")
        
        print("=" * 60)
    
    def executar_simulacao(self):
        """Executa simulação completa"""
        print("\n" + "=" * 60)
        print("🚀 SIMULADOR DE INTEGRAÇÃO MQTT")
        print("=" * 60)
        print("Este simulador demonstra como o sistema funcionaria")
        print("com comunicação MQTT real entre Python e HTML.")
        print("=" * 60)
        
        self.log_event("Simulador de integração iniciado")
        
        # Simula sequência de colisões
        sensores = ["sensor_frontal", "sensor_lateral_L", "sensor_lateral_R", "sensor_traseiro"]
        
        print("\n🎯 Simulando sequência de colisões...")
        
        for i in range(5):
            print(f"\n🚗 Simulando colisão #{i+1}...")
            
            # Simula colisão
            colisao = self.simular_colisao(random.choice(sensores))
            
            # Simula envio MQTT
            mensagem = self.simular_mensagem_mqtt(colisao)
            
            # Simula recebimento no sistema Python
            self.log_event("📥 Sistema Python recebeu mensagem MQTT")
            self.log_event("📊 Atualizando estatísticas...")
            self.log_event("💾 Salvando dados...")
            
            # Simula atualização na interface HTML
            self.log_event("🌐 Interface HTML atualizada")
            self.log_event("📈 Gráficos atualizados em tempo real")
            
            print(f"✅ Colisão #{i+1} processada com sucesso!")
            
            if i < 4:  # Não espera após a última
                time.sleep(2)
        
        # Salva dados finais
        self.salvar_dados()
        
        # Exibe estatísticas
        self.exibir_estatisticas()
        
        print("\n" + "=" * 60)
        print("✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("📁 Arquivos gerados:")
        print(f"  • Log: {self.log_file}")
        print(f"  • Dados: {self.data_file}")
        print("\n🔗 Para integração real:")
        print("  1. Configure broker MQTT acessível")
        print("  2. Execute: python detector_colisao.py")
        print("  3. Abra: detector-colisao.html")
        print("  4. Conecte ambos ao mesmo broker")
        print("=" * 60)

def main():
    """Função principal"""
    simulador = SimuladorIntegracao()
    
    try:
        simulador.executar_simulacao()
    except KeyboardInterrupt:
        print("\n\n⏹️ Simulação interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante a simulação: {e}")

if __name__ == "__main__":
    main()






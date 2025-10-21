#!/usr/bin/env python3
"""
Sistema Avançado de Detecção de Colisão via MQTT
Versão melhorada com logging, persistência de dados e interface aprimorada
"""

import sys
import os
import time
import json
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

# Imports externos
try:
    import paho.mqtt.client as mqtt
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Inicializa colorama
except ImportError as e:
    print(f"❌ ERRO: Biblioteca não encontrada: {e}")
    print("Para instalar as dependências, execute:")
    print("pip install -r requirements.txt")
    sys.exit(1)

# Importa configurações
try:
    from config import (
        MQTT_CONFIG, CONNECTION_CONFIG, LOGGING_CONFIG, 
        DATA_CONFIG, UI_CONFIG, STATS_CONFIG
    )
except ImportError:
    print("❌ ERRO: Arquivo config.py não encontrado!")
    print("Certifique-se de que o arquivo config.py está no mesmo diretório.")
    sys.exit(1)

class ColisaoDetector:
    """Classe principal para detecção de colisões via MQTT"""
    
    def __init__(self):
        self.conectado = False
        self.cliques_detectados = 0
        self.historico_colisoes: List[Dict] = []
        self.client: Optional[mqtt.Client] = None
        self.reconnect_attempts = 0
        self.last_ping_time = time.time()
        self.start_time = datetime.now()
        self.stats_lock = threading.Lock()
        
        # Configurações
        self.mqtt_config = MQTT_CONFIG
        self.conn_config = CONNECTION_CONFIG
        self.data_config = DATA_CONFIG
        self.ui_config = UI_CONFIG
        self.stats_config = STATS_CONFIG
        
        # Configura logging
        self._setup_logging()
        
        # Carrega dados salvos
        self._load_saved_data()
        
        # Thread para auto-save
        if self.data_config["save_to_file"]:
            self._start_auto_save()
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        log_config = LOGGING_CONFIG
        
        # Cria diretório de logs se não existir
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configura logging
        from logging.handlers import RotatingFileHandler
        
        logging.basicConfig(
            level=getattr(logging, log_config["level"]),
            format=log_config["format"],
            handlers=[
                RotatingFileHandler(
                    log_dir / log_config["file"],
                    maxBytes=log_config["max_size"],
                    backupCount=log_config["backup_count"]
                ),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Sistema de Detecção de Colisão iniciado")
    
    def _load_saved_data(self):
        """Carrega dados salvos do arquivo"""
        if not self.data_config["save_to_file"]:
            return
            
        data_file = Path(self.data_config["data_file"])
        if data_file.exists():
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.historico_colisoes = data.get('historico', [])
                    self.cliques_detectados = data.get('total_colisoes', 0)
                    self.logger.info(f"Dados carregados: {self.cliques_detectados} colisões")
            except Exception as e:
                self.logger.error(f"Erro ao carregar dados salvos: {e}")
    
    def _save_data(self):
        """Salva dados atuais no arquivo"""
        if not self.data_config["save_to_file"]:
            return
            
        try:
            data = {
                'total_colisoes': self.cliques_detectados,
                'historico': self.historico_colisoes[-self.data_config["max_history_size"]:],
                'last_save': datetime.now().isoformat()
            }
            
            with open(self.data_config["data_file"], 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            self.logger.debug("Dados salvos com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao salvar dados: {e}")
    
    def _start_auto_save(self):
        """Inicia thread para salvar dados automaticamente"""
        def auto_save_worker():
            while True:
                time.sleep(self.data_config["auto_save_interval"])
                self._save_data()
        
        save_thread = threading.Thread(target=auto_save_worker, daemon=True)
        save_thread.start()
    
    def _print_colored(self, message: str, color: str = Fore.WHITE, style: str = ""):
        """Imprime mensagem com cores"""
        if self.ui_config["use_colors"]:
            print(f"{style}{color}{message}{Style.RESET_ALL}")
        else:
            print(message)
    
    def _print_separator(self, char: str = None, length: int = None):
        """Imprime separador visual"""
        char = char or self.ui_config["separator_char"]
        length = length or self.ui_config["separator_length"]
        self._print_colored(char * length, Fore.CYAN)
    
    def _print_header(self, title: str):
        """Imprime cabeçalho formatado"""
        self._print_separator()
        self._print_colored(title, Fore.YELLOW, Style.BRIGHT)
        self._print_separator()
    
    def _check_connection_health(self):
        """Verifica saúde da conexão"""
        current_time = time.time()
        if current_time - self.last_ping_time > self.conn_config["ping_interval"]:
            if self.client and self.conectado:
                try:
                    # Verifica se a conexão ainda está ativa tentando publicar uma mensagem de ping
                    ping_topic = f"{self.mqtt_config['topic']}/ping"
                    ping_message = json.dumps({
                        "tipo": "ping",
                        "timestamp": current_time,
                        "client_id": self.mqtt_config['client_id']
                    })
                    
                    # Publica mensagem de ping (sem retenção)
                    result = self.client.publish(ping_topic, ping_message, qos=0, retain=False)
                    
                    if result.rc == mqtt.MQTT_ERR_SUCCESS:
                        self.last_ping_time = current_time
                        self.logger.debug("Ping enviado para verificar conexão")
                    else:
                        self.logger.warning(f"Falha ao enviar ping: {result.rc}")
                        
                except Exception as e:
                    self.logger.warning(f"Erro ao verificar conexão: {e}")
    
    def on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback executado quando conecta ao broker"""
        if rc == 0:
            self.conectado = True
            self.reconnect_attempts = 0
            self.last_ping_time = time.time()
            
            self._print_header("✅ CONECTADO AO MQTT BROKER COM SUCESSO!")
            self._print_colored(f"Broker: {self.mqtt_config['broker']}:{self.mqtt_config['port']}", Fore.GREEN)
            self._print_colored(f"Tópico: {self.mqtt_config['topic']}", Fore.GREEN)
            self._print_colored(f"Usuário: {self.mqtt_config['username']}", Fore.GREEN)
            self._print_colored(f"Client ID: {self.mqtt_config['client_id']}", Fore.GREEN)
            self._print_separator()
            
            # Inscrever no tópico
            client.subscribe(self.mqtt_config['topic'], qos=self.mqtt_config['qos'])
            self._print_colored(f"✓ Inscrito no tópico: {self.mqtt_config['topic']}", Fore.GREEN)
            
            self.logger.info("Conectado ao broker MQTT com sucesso")
        else:
            self.conectado = False
            codigos_erro = {
                1: "Versão do protocolo incorreta",
                2: "Identificador rejeitado", 
                3: "Servidor indisponível",
                4: "Usuário/senha incorretos",
                5: "Não autorizado"
            }
            error_msg = codigos_erro.get(rc, f'Código {rc}')
            self._print_colored(f"❌ Erro ao conectar: {error_msg}", Fore.RED)
            self.logger.error(f"Erro de conexão: {error_msg}")
    
    def on_disconnect(self, client, userdata, rc, properties=None):
        """Callback executado quando desconecta do broker"""
        self.conectado = False
        if rc != 0:
            self._print_colored(f"\n⚠️ Desconexão inesperada! (código {rc})", Fore.YELLOW)
            self.logger.warning(f"Desconexão inesperada: código {rc}")
            self._attempt_reconnect()
    
    def _attempt_reconnect(self):
        """Tenta reconectar automaticamente"""
        if self.reconnect_attempts < self.conn_config["max_reconnect_attempts"]:
            self.reconnect_attempts += 1
            delay = self.conn_config["reconnect_delay"] * self.reconnect_attempts
            
            self._print_colored(f"Tentando reconectar em {delay}s... (tentativa {self.reconnect_attempts})", Fore.YELLOW)
            self.logger.info(f"Tentativa de reconexão {self.reconnect_attempts}")
            
            time.sleep(delay)
            
            try:
                self.client.reconnect()
            except Exception as e:
                self.logger.error(f"Erro na reconexão: {e}")
        else:
            self._print_colored("❌ Máximo de tentativas de reconexão atingido!", Fore.RED)
            self.logger.error("Máximo de tentativas de reconexão atingido")
    
    def on_publish(self, client, userdata, mid, properties=None, reason_codes=None):
        """Callback executado quando publica mensagem"""
        self._print_colored(f"✓ Mensagem {mid} publicada com sucesso", Fore.GREEN)
        self.logger.debug(f"Mensagem {mid} publicada")
    
    def on_message(self, client, userdata, msg):
        """Recebe e processa mensagens do broker via MQTT"""
        try:
            payload = msg.payload.decode('utf-8')
            timestamp = datetime.now()
            
            # Tenta interpretar como JSON
            try:
                dados = json.loads(payload)
                tipo_msg = dados.get('tipo', '').lower()
                mensagem = dados.get('mensagem', payload)
                sensor_id = dados.get('sensor_id', 'desconhecido')
            except json.JSONDecodeError:
                tipo_msg = payload.lower()
                mensagem = payload
                sensor_id = 'desconhecido'
            
            # Detecta colisão
            if 'colisao' in tipo_msg or 'colisão' in tipo_msg or 'collision' in tipo_msg:
                with self.stats_lock:
                    self.cliques_detectados += 1
                    
                    # Armazena no histórico
                    registro = {
                        'numero': self.cliques_detectados,
                        'timestamp': timestamp.isoformat(),
                        'mensagem': mensagem,
                        'sensor_id': sensor_id,
                        'topic': msg.topic,
                        'qos': msg.qos
                    }
                    self.historico_colisoes.append(registro)
                    
                    # Mantém apenas os últimos registros em memória
                    if len(self.historico_colisoes) > self.data_config["max_history_size"]:
                        self.historico_colisoes = self.historico_colisoes[-self.data_config["max_history_size"]:]
                
                # Exibe informação formatada
                self._print_separator(length=50)
                self._print_colored(f"🔴 COLISÃO DETECTADA #{self.cliques_detectados}", Fore.RED, Style.BRIGHT)
                self._print_separator(length=50)
                
                if self.ui_config["show_timestamp"]:
                    self._print_colored(f"⏰ Horário: {timestamp.strftime(self.ui_config['date_format'])}", Fore.CYAN)
                
                if self.ui_config["show_topic"]:
                    self._print_colored(f"📍 Tópico: {msg.topic}", Fore.CYAN)
                
                if self.ui_config["show_message"]:
                    self._print_colored(f"📝 Mensagem: {mensagem}", Fore.CYAN)
                
                self._print_colored(f"🆔 Sensor: {sensor_id}", Fore.CYAN)
                self._print_colored(f"📊 Total acumulado: {self.cliques_detectados} colisões", Fore.YELLOW)
                
                # Verifica alerta de taxa alta
                self._check_alert_threshold()
                
                self._print_separator(length=50)
                
                self.logger.info(f"Colisão #{self.cliques_detectados} detectada: {mensagem}")
            else:
                # Mensagem que não é colisão
                self._print_colored(f"ℹ️ Mensagem recebida: {payload[:100]}", Fore.BLUE)
                self.logger.debug(f"Mensagem não-colisão recebida: {payload[:100]}")
                
        except Exception as e:
            error_msg = f"Erro ao processar mensagem: {e}"
            self._print_colored(f"❌ {error_msg}", Fore.RED)
            self.logger.error(error_msg)
    
    def _check_alert_threshold(self):
        """Verifica se a taxa de colisões está acima do limite"""
        if not self.stats_config["alert_threshold"]:
            return
            
        # Calcula taxa dos últimos 60 segundos
        now = datetime.now()
        recent_colisoes = [
            col for col in self.historico_colisoes 
            if (now - datetime.fromisoformat(col['timestamp'])).total_seconds() <= 60
        ]
        
        if len(recent_colisoes) > self.stats_config["alert_threshold"]:
            self._print_colored(
                f"⚠️ ALERTA: {len(recent_colisoes)} colisões no último minuto!", 
                Fore.RED, Style.BRIGHT
            )
            self.logger.warning(f"Taxa alta de colisões: {len(recent_colisoes)} no último minuto")
    
    def exibir_estatisticas_avancadas(self):
        """Exibe estatísticas avançadas das colisões detectadas"""
        if self.cliques_detectados == 0:
            self._print_colored("\nNenhuma colisão foi detectada durante a execução.", Fore.YELLOW)
            return
        
        self._print_header("📊 ESTATÍSTICAS AVANÇADAS")
        
        # Estatísticas básicas
        self._print_colored(f"Total de colisões: {self.cliques_detectados}", Fore.GREEN)
        
        if self.historico_colisoes:
            primeira = datetime.fromisoformat(self.historico_colisoes[0]['timestamp'])
            ultima = datetime.fromisoformat(self.historico_colisoes[-1]['timestamp'])
            duracao_total = (ultima - primeira).total_seconds()
            duracao_execucao = (datetime.now() - self.start_time).total_seconds()
            
            self._print_colored(f"Primeira colisão: {primeira.strftime(self.ui_config['date_format'])}", Fore.CYAN)
            self._print_colored(f"Última colisão: {ultima.strftime(self.ui_config['date_format'])}", Fore.CYAN)
            self._print_colored(f"Tempo de execução: {duracao_execucao/60:.1f} minutos", Fore.CYAN)
            
            # Taxas
            if self.stats_config["show_rate_per_minute"] and duracao_total > 0:
                taxa_minuto = self.cliques_detectados / (duracao_total / 60)
                self._print_colored(f"Taxa média: {taxa_minuto:.2f} colisões/minuto", Fore.YELLOW)
            
            if self.stats_config["show_rate_per_hour"] and duracao_total > 0:
                taxa_hora = self.cliques_detectados / (duracao_total / 3600)
                self._print_colored(f"Taxa por hora: {taxa_hora:.2f} colisões/hora", Fore.YELLOW)
            
            # Análise por hora
            if self.stats_config["show_peak_hour"]:
                colisoes_por_hora = {}
                for colisao in self.historico_colisoes:
                    hora = datetime.fromisoformat(colisao['timestamp']).hour
                    colisoes_por_hora[hora] = colisoes_por_hora.get(hora, 0) + 1
                
                if colisoes_por_hora:
                    hora_pico = max(colisoes_por_hora, key=colisoes_por_hora.get)
                    self._print_colored(f"Hora de pico: {hora_pico:02d}:00 ({colisoes_por_hora[hora_pico]} colisões)", Fore.MAGENTA)
            
            # Intervalo médio entre colisões
            if self.stats_config["show_average_interval"] and len(self.historico_colisoes) > 1:
                intervalos = []
                for i in range(1, len(self.historico_colisoes)):
                    t1 = datetime.fromisoformat(self.historico_colisoes[i-1]['timestamp'])
                    t2 = datetime.fromisoformat(self.historico_colisoes[i]['timestamp'])
                    intervalos.append((t2 - t1).total_seconds())
                
                if intervalos:
                    intervalo_medio = sum(intervalos) / len(intervalos)
                    self._print_colored(f"Intervalo médio: {intervalo_medio:.1f} segundos", Fore.MAGENTA)
            
            # Sensores mais ativos
            sensores = {}
            for colisao in self.historico_colisoes:
                sensor = colisao.get('sensor_id', 'desconhecido')
                sensores[sensor] = sensores.get(sensor, 0) + 1
            
            if sensores:
                self._print_colored("\n📡 Sensores mais ativos:", Fore.CYAN)
                for sensor, count in sorted(sensores.items(), key=lambda x: x[1], reverse=True)[:5]:
                    self._print_colored(f"  {sensor}: {count} colisões", Fore.CYAN)
        
        self._print_separator()
        self.logger.info("Estatísticas exibidas")
    
    def conectar(self):
        """Conecta ao broker MQTT"""
        try:
            self._print_header("🚀 SISTEMA AVANÇADO DE DETECÇÃO DE COLISÃO - MQTT")
            self._print_colored(f"\n📡 Conectando ao MQTT Broker: {self.mqtt_config['broker']}:{self.mqtt_config['port']}", Fore.CYAN)
            
            # Configura cliente MQTT
            self.client = mqtt.Client(
                mqtt.CallbackAPIVersion.VERSION2, 
                client_id=self.mqtt_config['client_id'],
                clean_session=self.mqtt_config['clean_session']
            )
            
            # Configura autenticação se necessário
            if self.mqtt_config['username'] and self.mqtt_config['password']:
                self.client.username_pw_set(
                    self.mqtt_config['username'], 
                    self.mqtt_config['password']
                )
            
            # Configura callbacks
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_publish = self.on_publish
            self.client.on_message = self.on_message
            
            # Conecta ao broker
            self.client.connect(
                self.mqtt_config['broker'], 
                self.mqtt_config['port'], 
                keepalive=self.mqtt_config['keepalive']
            )
            self.client.loop_start()
            
            # Aguarda conexão
            timeout = self.conn_config["timeout"]
            inicio = time.time()
            while not self.conectado and (time.time() - inicio) < timeout:
                time.sleep(0.1)
            
            return self.conectado
            
        except Exception as e:
            error_msg = f"Erro fatal na conexão: {e}"
            self._print_colored(f"❌ {error_msg}", Fore.RED)
            self.logger.error(error_msg)
            return False
    
    def executar(self):
        """Executa o sistema principal"""
        if not self.conectar():
            self._print_colored(f"❌ Erro: Não conseguiu conectar ao MQTT em {self.conn_config['timeout']}s", Fore.RED)
            self._print_colored("Verifique sua conexão com a internet e tente novamente.", Fore.YELLOW)
            return
        
        self._print_colored("✓ Sistema pronto! Aguardando mensagens de colisão...", Fore.GREEN)
        self._print_colored("💡 Pressione CTRL+C para sair", Fore.CYAN)
        self.logger.info("Sistema em execução")
        
        try:
            while True:
                time.sleep(1)
                self._check_connection_health()
                
        except KeyboardInterrupt:
            self._print_colored("\n\n⏹️ Programa encerrado pelo usuário", Fore.YELLOW)
            self.exibir_estatisticas_avancadas()
            self.logger.info("Programa encerrado pelo usuário")
        
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """Limpa recursos ao encerrar"""
        if self.client:
            self._print_colored("\n🔌 Desconectando do broker...", Fore.CYAN)
            self.client.loop_stop()
            self.client.disconnect()
            time.sleep(1)
        
        # Salva dados finais
        if self.data_config["save_to_file"]:
            self._save_data()
            self._print_colored("✓ Dados salvos", Fore.GREEN)
        
        self._print_colored("✓ Desconectado do MQTT", Fore.GREEN)
        self.logger.info("Sistema encerrado")

def main():
    """Função principal"""
    try:
        detector = ColisaoDetector()
        detector.executar()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        logging.error(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
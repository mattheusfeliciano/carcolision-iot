# 🚀 Sistema Avançado de Detecção de Colisão via MQTT

Um sistema robusto e profissional para detecção de colisões em tempo real usando o protocolo MQTT, com recursos avançados de logging, persistência de dados e análise estatística.

## ✨ Principais Melhorias Implementadas

### 🔧 **Arquitetura Melhorada**
- **Programação Orientada a Objetos** - Código mais organizado e manutenível
- **Arquivo de configuração separado** - Facilita customizações sem modificar código
- **Sistema de logging profissional** - Logs detalhados com rotação automática
- **Tratamento robusto de erros** - Reconexão automática e recuperação de falhas

### 📊 **Recursos Avançados**
- **Persistência de dados** - Histórico salvo automaticamente em arquivo JSON
- **Estatísticas avançadas** - Análise de taxas, horários de pico e intervalos
- **Monitoramento de saúde** - Ping automático para verificar conexão
- **Sistema de alertas** - Notificações quando taxa de colisões é alta
- **Interface colorida** - Saída visual melhorada com cores e formatação

### 🛡️ **Confiabilidade**
- **Reconexão automática** - Tenta reconectar automaticamente em caso de falha
- **Thread-safe** - Operações seguras para múltiplas threads
- **Backup de dados** - Logs com rotação automática
- **Validação de entrada** - Tratamento seguro de mensagens malformadas

## 📁 Estrutura do Projeto

```
projeto/
├── detector_colisao.py    # Sistema principal melhorado
├── config.py              # Configurações centralizadas
├── requirements.txt       # Dependências do projeto
├── README.md             # Esta documentação
├── logs/                 # Diretório de logs (criado automaticamente)
│   └── colisao.log       # Arquivo de log principal
└── historico_colisoes.json # Histórico persistido (criado automaticamente)
```

## 🚀 Instalação e Uso

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar o Sistema
Edite o arquivo `config.py` para ajustar:
- **Broker MQTT** e credenciais
- **Tópicos** para monitorar
- **Configurações de logging**
- **Parâmetros de interface**

### 3. Executar o Sistema
```bash
python detector_colisao.py
```

## ⚙️ Configurações Principais

### MQTT
```python
MQTT_CONFIG = {
    "broker": "mqtt.eclipseprojects.io",
    "port": 1883,
    "username": "vini123",
    "topic": "vini123/colisao",
    "qos": 1,  # Quality of Service
}
```

### Logging
```python
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "colisao.log",
    "max_size": 10485760,  # 10MB
    "backup_count": 5
}
```

### Interface
```python
UI_CONFIG = {
    "use_colors": True,
    "show_timestamp": True,
    "date_format": "%d/%m/%Y %H:%M:%S"
}
```

## 📈 Estatísticas Disponíveis

O sistema agora fornece análises detalhadas:

- **Taxa de colisões** por minuto e por hora
- **Horário de pico** - quando mais colisões ocorrem
- **Intervalo médio** entre colisões
- **Sensores mais ativos** - ranking por frequência
- **Tempo de execução** e duração total
- **Alertas automáticos** para taxas altas

## 🔍 Exemplo de Saída

```
============================================================
✅ CONECTADO AO MQTT BROKER COM SUCESSO!
============================================================
Broker: mqtt.eclipseprojects.io:1883
Tópico: vini123/colisao
Usuário: vini123
Client ID: detector_colisao_pc
============================================================
✓ Inscrito no tópico: vini123/colisao

==================================================
🔴 COLISÃO DETECTADA #1
==================================================
⏰ Horário: 15/12/2024 14:30:25
📍 Tópico: vini123/colisao
📝 Mensagem: Colisão detectada no sensor A
🆔 Sensor: sensor_a
📊 Total acumulado: 1 colisões
==================================================
```

## 🛠️ Recursos Técnicos

### Logging Profissional
- **Múltiplos níveis**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Rotação automática** de arquivos de log
- **Logs estruturados** com timestamps e contexto
- **Arquivo e console** simultaneamente

### Persistência de Dados
- **Auto-save** a cada 30 segundos
- **Carregamento automático** ao iniciar
- **Histórico limitado** em memória (1000 registros)
- **Backup completo** em JSON

### Monitoramento de Saúde
- **Ping automático** a cada 30 segundos
- **Detecção de desconexões**
- **Reconexão inteligente** com backoff exponencial
- **Máximo de tentativas** configurável

## 🔧 Personalização

### Adicionar Novos Tipos de Mensagem
```python
# No método on_message, adicione novas condições:
if 'emergencia' in tipo_msg:
    # Processar emergência
elif 'manutencao' in tipo_msg:
    # Processar manutenção
```

### Modificar Estatísticas
```python
# No arquivo config.py, ajuste STATS_CONFIG:
STATS_CONFIG = {
    "show_rate_per_minute": True,
    "alert_threshold": 5,  # Alerta com 5+ colisões/min
}
```

### Customizar Interface
```python
# Modifique UI_CONFIG para personalizar cores e formato:
UI_CONFIG = {
    "separator_char": "*",
    "separator_length": 80,
    "use_colors": False  # Desabilita cores
}
```

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de conexão MQTT**
   - Verifique conexão com internet
   - Confirme broker e porta no `config.py`
   - Teste credenciais se necessário

2. **Bibliotecas não encontradas**
   ```bash
   pip install paho-mqtt colorama
   ```

3. **Logs não aparecem**
   - Verifique permissões de escrita
   - Confirme nível de log no `config.py`

4. **Dados não salvam**
   - Verifique permissões de escrita
   - Confirme `save_to_file: True` no `config.py`

## 📝 Changelog

### v2.0 - Sistema Avançado
- ✅ Arquitetura OOP completa
- ✅ Sistema de logging profissional
- ✅ Persistência de dados automática
- ✅ Estatísticas avançadas
- ✅ Interface colorida melhorada
- ✅ Reconexão automática robusta
- ✅ Monitoramento de saúde da conexão
- ✅ Sistema de alertas configurável

### v1.0 - Sistema Básico
- ✅ Detecção básica de colisões via MQTT
- ✅ Estatísticas simples
- ✅ Interface texto simples

## 🤝 Contribuição

Para contribuir com melhorias:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Implemente as melhorias
4. Teste thoroughly
5. Submeta um pull request

## 📄 Licença

Este projeto é de código aberto. Use e modifique conforme necessário para seus projetos.

---

**Desenvolvido com ❤️ para sistemas IoT robustos e confiáveis**



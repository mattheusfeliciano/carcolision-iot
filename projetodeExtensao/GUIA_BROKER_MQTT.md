# 🚀 GUIA COMPLETO: Configuração de Broker MQTT

## 📋 Opções de Broker MQTT

### **1. Broker Local (Recomendado para desenvolvimento)**
### **2. Broker na Nuvem (Para produção)**
### **3. Broker Docker (Fácil de configurar)**

---

## 🏠 **OPÇÃO 1: Broker Local com Mosquitto**

### **Passo 1: Instalar Mosquitto**

#### **Windows:**
```bash
# Baixar Mosquitto do site oficial
# https://mosquitto.org/download/

# Ou usar Chocolatey:
choco install mosquitto

# Ou usar Scoop:
scoop install mosquitto
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

#### **macOS:**
```bash
brew install mosquitto
```

### **Passo 2: Configurar Mosquitto**

#### **Criar arquivo de configuração:**
```bash
# Windows: C:\Program Files\mosquitto\mosquitto.conf
# Linux: /etc/mosquitto/mosquitto.conf
```

#### **Conteúdo do arquivo mosquitto.conf:**
```conf
# Configuração básica do Mosquitto
port 1883
listener 8081
protocol websockets

# Logs
log_dest file C:\mosquitto\mosquitto.log
log_type error
log_type warning
log_type notice
log_type information

# Persistência
persistence true
persistence_location C:\mosquitto\data\

# Autenticação (opcional)
# password_file C:\mosquitto\passwd
# allow_anonymous true

# Configurações de segurança
max_inflight_messages 20
max_queued_messages 100
```

### **Passo 3: Iniciar o Broker**

#### **Windows:**
```bash
# Como serviço
net start mosquitto

# Ou manualmente
"C:\Program Files\mosquitto\mosquitto.exe" -c mosquitto.conf
```

#### **Linux:**
```bash
# Iniciar serviço
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

# Verificar status
sudo systemctl status mosquitto
```

### **Passo 4: Testar Conexão**
```bash
# Terminal 1 - Subscriber
mosquitto_sub -h localhost -t "teste/topico"

# Terminal 2 - Publisher
mosquitto_pub -h localhost -t "teste/topico" -m "Olá MQTT!"
```

---

## ☁️ **OPÇÃO 2: Broker na Nuvem**

### **Brokers Gratuitos:**

#### **1. Eclipse Mosquitto (Público)**
- **Host:** mqtt.eclipseprojects.io
- **Porta:** 1883 (TCP) / 8081 (WebSocket)
- **Limitações:** Sem autenticação, uso público

#### **2. HiveMQ (Público)**
- **Host:** broker.hivemq.com
- **Porta:** 1883 (TCP) / 8000 (WebSocket)
- **Limitações:** Sem autenticação, uso público

#### **3. EMQX (Público)**
- **Host:** broker.emqx.io
- **Porta:** 1883 (TCP) / 8083 (WebSocket)
- **Limitações:** Sem autenticação, uso público

### **Brokers Pagos (Produção):**

#### **1. AWS IoT Core**
- **Vantagens:** Escalável, seguro, integrado
- **Preço:** Pay-per-use
- **Setup:** Console AWS

#### **2. Azure IoT Hub**
- **Vantagens:** Integração Microsoft, analytics
- **Preço:** Pay-per-use
- **Setup:** Portal Azure

#### **3. Google Cloud IoT Core**
- **Vantagens:** Machine Learning, BigQuery
- **Preço:** Pay-per-use
- **Setup:** Console GCP

---

## 🐳 **OPÇÃO 3: Broker Docker (Mais Fácil)**

### **Passo 1: Instalar Docker**
```bash
# Baixar Docker Desktop
# https://www.docker.com/products/docker-desktop
```

### **Passo 2: Criar docker-compose.yml**
```yaml
version: '3.8'

services:
  mosquitto:
    image: eclipse-mosquitto:latest
    container_name: mqtt-broker
    ports:
      - "1883:1883"    # MQTT TCP
      - "8081:8081"    # MQTT WebSocket
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./data:/mosquitto/data
      - ./logs:/mosquitto/log
    restart: unless-stopped
    command: mosquitto -c /mosquitto/config/mosquitto.conf

  mqtt-explorer:
    image: smeagolworms4/mqtt-explorer:latest
    container_name: mqtt-explorer
    ports:
      - "4000:4000"
    depends_on:
      - mosquitto
    restart: unless-stopped
```

### **Passo 3: Criar mosquitto.conf**
```conf
listener 1883
listener 8081
protocol websockets

allow_anonymous true

persistence true
persistence_location /mosquitto/data/

log_dest file /mosquitto/log/mosquitto.log
log_type all
```

### **Passo 4: Executar**
```bash
# Iniciar broker
docker-compose up -d

# Verificar logs
docker-compose logs -f mosquitto

# Parar broker
docker-compose down
```

---

## 🔧 **CONFIGURAÇÃO DO SEU PROJETO**

### **Passo 1: Atualizar config.py**

#### **Para Broker Local:**
```python
MQTT_CONFIG = {
    "broker": "localhost",  # ou "127.0.0.1"
    "port": 1883,
    "keepalive": 60,
    "username": None,  # Deixe None se não usar auth
    "password": None,
    "client_id": "detector_colisao_pc",
    "topic": "vini123/colisao",
    "qos": 1,
    "retain": False,
    "clean_session": True
}
```

#### **Para Broker WebSocket (HTML):**
```python
# No HTML, use:
# Porta: 8081 (WebSocket)
# Protocolo: ws:// ou wss://
```

### **Passo 2: Testar Conexão**

#### **Script de Teste:**
```python
import paho.mqtt.client as mqtt
import time

def test_connection():
    client = mqtt.Client()
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("✅ Conectado ao broker!")
        else:
            print(f"❌ Erro: {rc}")
    
    client.on_connect = on_connect
    client.connect("localhost", 1883, 60)
    client.loop_start()
    time.sleep(2)
    client.disconnect()

test_connection()
```

---

## 🛠️ **CONFIGURAÇÃO AVANÇADA**

### **Autenticação com Usuário/Senha:**

#### **1. Criar usuários:**
```bash
# Instalar mosquitto_passwd
mosquitto_passwd -c passwd usuario1
# Digite a senha quando solicitado
```

#### **2. Atualizar mosquitto.conf:**
```conf
password_file /path/to/passwd
allow_anonymous false
```

#### **3. Atualizar config.py:**
```python
MQTT_CONFIG = {
    "broker": "localhost",
    "port": 1883,
    "username": "usuario1",
    "password": "sua_senha",
    # ... resto da configuração
}
```

### **SSL/TLS (Segurança):**

#### **1. Gerar certificados:**
```bash
# Gerar CA
openssl req -new -x509 -days 365 -extensions v3_ca -keyout ca.key -out ca.crt

# Gerar certificado do broker
openssl genrsa -out broker.key 2048
openssl req -out broker.csr -key broker.key -new
openssl x509 -req -in broker.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out broker.crt -days 365
```

#### **2. Atualizar mosquitto.conf:**
```conf
listener 8883
cafile /path/to/ca.crt
certfile /path/to/broker.crt
keyfile /path/to/broker.key
```

#### **3. Atualizar config.py:**
```python
MQTT_CONFIG = {
    "broker": "localhost",
    "port": 8883,  # Porta SSL
    "use_ssl": True,
    # ... resto da configuração
}
```

---

## 🧪 **TESTE COMPLETO**

### **Passo 1: Iniciar Broker**
```bash
# Docker (recomendado)
docker-compose up -d

# Ou Mosquitto local
mosquitto -c mosquitto.conf
```

### **Passo 2: Testar Python**
```bash
python detector_colisao.py
```

### **Passo 3: Testar HTML**
```bash
# Abrir detector-colisao.html no navegador
# Configurar: localhost:8081
# Conectar e testar
```

### **Passo 4: Monitorar**
```bash
# Ver logs do broker
docker-compose logs -f mosquitto

# Ou arquivo de log
tail -f mosquitto.log
```

---

## 🎯 **RECOMENDAÇÃO FINAL**

### **Para Desenvolvimento:**
1. **Use Docker** com Mosquitto (mais fácil)
2. **Configure WebSocket** na porta 8081
3. **Deixe sem autenticação** inicialmente
4. **Monitore logs** para debug

### **Para Produção:**
1. **Use broker na nuvem** (AWS/Azure/GCP)
2. **Configure SSL/TLS**
3. **Implemente autenticação**
4. **Configure backup** e monitoramento

### **Comandos Rápidos:**
```bash
# Iniciar broker Docker
docker-compose up -d

# Testar conexão
python teste_conectividade.py

# Executar sistema
python detector_colisao.py

# Abrir interface
start detector-colisao.html
```

**Agora você tem um broker MQTT funcionando!** 🎉






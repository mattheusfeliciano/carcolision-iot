# Imagem base do Python
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos do projeto para dentro do container
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000 (para acesso via navegador)
EXPOSE 5000

# Comando principal: roda o servidor Flask + detector
CMD ["python", "web_server.py"]


# Usa uma imagem Python leve, mas com as ferramentas de compilação necessárias
FROM python:3.10-slim-bullseye

# Instala as dependências do sistema necessárias para o dlib e opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    libv4l-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Expõe a porta que o Flask/Gunicorn vai usar
EXPOSE 10000

# Comando para rodar a aplicação usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
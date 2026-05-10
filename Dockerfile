# Usamos uma imagem que já tem dlib e face_recognition pré-instalados e otimizados
FROM animcogn/face_recognition:cpu

# Define o diretório de trabalho
WORKDIR /app

# Copia apenas o arquivo de requisitos
COPY requirements.txt .

# Atualiza o pip e instala as dependências
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# A porta padrão do Render para Docker é 10000
EXPOSE 10000

# Comando para rodar a aplicação usando Gunicorn
CMD python database.py && gunicorn --bind 0.0.0.0:10000 app:app
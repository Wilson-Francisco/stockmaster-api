# 1. Usa uma imagem oficial leve do Python como base
FROM python:3.11-slim

# 2. Define a pasta padrão de trabalho dentro do container
WORKDIR /app

# 3. Instala dependências do sistema necessárias para compilar o driver do PostgreSQL (psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia o arquivo de requerimentos para dentro do container
COPY requirements.txt .

# 5. Instala todas as bibliotecas Python listadas
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o código fonte da pasta app para dentro do container
COPY app/ ./app/

# 7. Expõe a porta padrão que a nossa API vai rodar
EXPOSE 8000

# 8. Comando oficial para ligar o servidor Uvicorn quando o container iniciar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use a imagem base do Python
FROM python:3.9

# Configure as variáveis de ambiente (altere conforme necessário)
ENV DJANGO_SETTINGS_MODULE=tracking.settings
ENV DEBUG=False
ENV PYTHONPATH=/app

# Crie o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt para o container
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o restante do código-fonte para o container
COPY . .

# Execute as migrações
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Alterar a porta para 80, se necessário
EXPOSE 80

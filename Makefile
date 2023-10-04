# Variáveis
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python
GUNICORN_CMD=${VENV_NAME}/bin/gunicorn
NGINX_CMD=sudo service nginx
REDIS_CMD=redis-server
CELERY_CMD=${PYTHON} -m celery -A tracking worker --loglevel=info
CELERY_BEAT_CMD=${PYTHON} -m celery -A tracking beat --loglevel=info

# Verifica se o comando Redis está disponível
REDIS_INSTALLED := $(shell command -v $(REDIS_CMD) 2> /dev/null)
OS := $(shell uname -s)

# Comandos padrões
.PHONY: install configure start stop migrations check_redis start_redis start_celery start_celery_beat

install-venv:
	@echo "Instalando python3-venv..."
ifeq ($(OS),Darwin)
	brew install python3-venv
else ifeq ($(OS),Linux)
	sudo apt update && sudo apt install python3-venv
endif

# Instala todas as dependências
install: install-venv
	@echo "Criando ambiente virtual..."
	python3 -m venv ${VENV_NAME}
	@echo "Instalando dependências..."
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install -r requirements.txt
	${PYTHON} -m pip install gunicorn
	@echo "Verificando instalação do Redis..."
ifndef REDIS_INSTALLED
	@echo "Redis não encontrado. Instalando..."
	sudo apt update && sudo apt install redis-server
else
	@echo "Redis já está instalado."
endif
	@echo "Tudo instalado!"

# Configura o projeto
configure:
	@echo "Aplicando migrações..."
	${PYTHON} manage.py makemigrations
	${PYTHON} manage.py migrate
	@echo "Configurando NGINX..."
	sudo cp . /etc/nginx/sites-available/project-tracking-code
	sudo ln -s /etc/nginx/sites-available/project-tracking-code /etc/nginx/sites-enabled
	sudo nginx -t
	@echo "Configuração completa!"

# Inicia todos os serviços necessários
start:
	@echo "Iniciando Redis..."
	nohup $(REDIS_CMD) > /dev/null 2>&1 &
	@echo "Iniciando Gunicorn..."
	nohup ${GUNICORN_CMD} tracking.wsgi:application --bind 0.0.0.0:8000 > /dev/null 2>&1 &
	@echo "Iniciando NGINX..."
	${NGINX_CMD} start
	@echo "Iniciando Celery..."
	nohup ${CELERY_CMD} > /dev/null 2>&1 &
	@echo "Iniciando Celery Beat..."
	nohup ${CELERY_BEAT_CMD} > /dev/null 2>&1 &
	@echo "Todos os serviços estão em execução!"

# Para todos os serviços
stop:
	@echo "Parando NGINX..."
	${NGINX_CMD} stop
	@echo "Parando Gunicorn..."
	pkill gunicorn
	@echo "Parando Redis..."
	pkill redis-server
	@echo "Parando Celery..."
	pkill -9 -f 'celery worker'
	@echo "Parando Celery Beat..."
	pkill -9 -f 'celery beat'
	@echo "Todos os serviços foram parados!"

# Aplica as migrações do Django
migrations:
	@echo "Criando migrações..."
	${PYTHON} manage.py makemigrations
	@echo "Aplicando migrações..."
	${PYTHON} manage.py migrate

# Verifica se o Redis está instalado
check_redis:
ifndef REDIS_INSTALLED
	$(error "Redis não está instalado. Por favor, execute 'make install' primeiro.")
endif

# Inicia o servidor Redis
start_redis: check_redis
	@echo "Iniciando Redis..."
	$(REDIS_CMD) &


app:
	@echo "Configurando o serviço systemd para a aplicação..."
	@echo "[Unit]" > tracking_app.service
	@echo "Description=Mega Rastreio" >> tracking_app.service
	@echo "After=network.target" >> tracking_app.service
	@echo "" >> tracking_app.service
	@echo "[Service]" >> tracking_app.service
	@echo "User=$(USER)" >> tracking_app.service
	@echo "WorkingDirectory=$(PWD)" >> tracking_app.service
	@echo "ExecStart=$(PWD)/${VENV_NAME}/bin/gunicorn --workers 3 tracking.wsgi:application --bind 0.0.0.0:8000" >> tracking_app.service
	@echo "" >> tracking_app.service
	@echo "[Install]" >> tracking_app.service
	@echo "WantedBy=multi-user.target" >> tracking_app.service
	@echo "" >> tracking_app.service
	sudo mv tracking_app.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl start tracking_app
	sudo systemctl enable tracking_app
	@echo "A aplicação está configurada para iniciar com o sistema."

drop-app:
	@echo "Removendo o serviço systemd da aplicação..."
	sudo systemctl stop tracking_app
	sudo systemctl disable tracking_app
	sudo rm /etc/systemd/system/tracking_app.service
	sudo systemctl daemon-reload
	sudo systemctl reset-failed
	@echo "O serviço da aplicação foi removido com sucesso."


ssl:
	# Instalar o Certbot
	sudo apt-get update
	sudo apt-get install -y software-properties-common
	sudo add-apt-repository ppa:certbot/certbot -y
	sudo apt-get update
	sudo apt-get install -y certbot python-certbot-nginx

	# Obter o certificado SSL usando o Certbot
	sudo certbot --nginx

	# Configurar a renovação automática do certificado SSL
	echo "0 0,12 * * * root python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew -q" | sudo tee -a /etc/crontab > /dev/null

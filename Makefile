# Variáveis
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python
GUNICORN_CMD=${VENV_NAME}/bin/gunicorn
NGINX_CMD=sudo service nginx
REDIS_CMD=redis-server
CELERY_CMD=${PYTHON} -m celery -A tracking worker --loglevel=info
CELERY_BEAT_CMD=${PYTHON} -m celery -A tracking beat --loglevel=info

REDIS_INSTALLED := $(shell command -v redis-server 2> /dev/null)
VENV_EXISTS := $(wildcard ${VENV_NAME}/bin/activate)
OS := $(shell uname -s)

.PHONY: install configure start stop migrations 

install: 
	@if [ -z $(VENV_EXISTS) ]; then \
		echo "Instalando python3-venv..."; \
		if [ $(OS) = "Darwin" ]; then brew install python3-venv; \
		elif [ $(OS) = "Linux" ]; then sudo apt update && sudo apt install python3-venv; \
		fi; \
		echo "Criando ambiente virtual..."; \
		python3 -m venv ${VENV_NAME}; \
	fi

	@echo "Instalando dependências..."
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install -r requirements.txt gunicorn

	@if [ -z $(REDIS_INSTALLED) ]; then \
		echo "Redis não encontrado. Instalando..."; \
		sudo apt update && sudo apt install redis-server; \
	else echo "Redis já está instalado."; \
	fi

configure:
	@echo "Aplicando migrações..."
	${PYTHON} manage.py makemigrations
	${PYTHON} manage.py migrate

	@if [ ! -d "/etc/nginx/sites-available/project-tracking-code" ]; then \
		echo "Configurando NGINX..."; \
		sudo cp -r . /etc/nginx/sites-available/project-tracking-code; \
		sudo ln -s /etc/nginx/sites-available/project-tracking-code /etc/nginx/sites-enabled; \
		sudo nginx -t; \
	fi

start: 
	@echo "Iniciando serviços..."
	nohup $(REDIS_CMD) > /dev/null 2>&1 &
	nohup ${GUNICORN_CMD} tracking.wsgi:application --bind 0.0.0.0:8000 > /dev/null 2>&1 &
	${NGINX_CMD} start
	nohup ${CELERY_CMD} > /dev/null 2>&1 &
	nohup ${CELERY_BEAT_CMD} > /dev/null 2>&1 &
	@echo "Todos os serviços estão em execução!"

stop:
	@echo "Parando serviços..."
	${NGINX_CMD} stop
	pkill gunicorn
	pkill redis-server
	pkill -9 -f 'celery worker'
	pkill -9 -f 'celery beat'
	@echo "Todos os serviços foram parados!"

migrations:
	@echo "Criando e aplicando migrações..."
	${PYTHON} manage.py makemigrations
	${PYTHON} manage.py migrate

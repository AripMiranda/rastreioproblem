# Variáveis
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python
REDIS_CMD=redis-server
CELERY_CMD=${PYTHON} -m celery -A tracking worker --loglevel=info
CELERY_BEAT_CMD=${PYTHON} -m celery -A tracking beat --loglevel=info

# Verifica se o comando Redis está disponível
REDIS_INSTALLED := $(shell command -v $(REDIS_CMD) 2> /dev/null)
OS := $(shell uname -s)

# Comandos padrões
.PHONY: install run migrations check_redis start_redis start_celery start_celery_beat


# Instala todas as dependências
install:
	@echo "Criando ambiente virtual..."
	python3 -m venv ${VENV_NAME}
	@echo "Instalando dependências..."
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install -r requirements.txt
	@echo "Verificando instalação do Redis..."
ifndef REDIS_INSTALLED
	@echo "Redis não encontrado. Instalando..."
ifeq ($(OS),Darwin)
	brew install redis
else ifeq ($(OS),Linux)
	if [ -f /etc/lsb-release ] || [ -f /etc/debian_version ]; then sudo apt update && sudo apt install redis-server; elif [ -f /etc/redhat-release ]; then sudo dnf install redis; fi
endif
else
	@echo "Redis já está instalado."
endif
	@echo "Tudo instalado!"

# Inicia o servidor do Django
run:
	@echo "Iniciando o servidor Django..."
	${PYTHON} manage.py runserver 0.0.0.0:8000

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
start_redis:
	@echo "Iniciando Redis..."
	$(REDIS_CMD) &


# README do Projeto Django: Rastreador de Produtos

## Visão Geral

Este projeto é um rastreador de produtos desenvolvido utilizando o framework Django em Python.

## Pré-requisitos

Antes de executar qualquer comando, certifique-se de que os seguintes softwares estejam instalados em sua máquina:

- Python 3.x
- pip
- Redis

Para obter mais detalhes sobre os requisitos, consulte o arquivo `requirements.txt`.

### Instalando o Redis

Caso o Redis não esteja instalado em sua máquina, você pode fazê-lo executando o seguinte comando:

**Mac (utilizando Homebrew):**

```bash
brew install redis
```

**Linux (Debian/Ubuntu):**

```bash
sudo apt update
sudo apt install redis-server
```

**Linux (Red Hat/Fedora):**

```bash
sudo dnf install redis
```

## Configuração do Ambiente Virtual

Este projeto utiliza um ambiente virtual para isolar as dependências do Python. Você pode criar o ambiente virtual e
instalar as dependências executando o seguinte comando:

```bash
make install
```

Isso criará um ambiente virtual na pasta `venv`, atualizará o `pip` e instalará todas as dependências listadas no
arquivo `requirements.txt`.

## Executando o Servidor Django

Para iniciar o servidor Django, utilize o seguinte comando:

```bash
make run
```

Este comando também verifica se o Redis está instalado e inicia um servidor Redis, se necessário.

## Aplicando Migrações

Para aplicar migrações ao banco de dados, execute o seguinte comando:

```bash
make migrations
```

Este comando criará migrações para as alterações no modelo de banco de dados e, em seguida, aplicará essas migrações.

## Uso do Celery com Redis

Este projeto utiliza o Celery para tarefas assíncronas e agendadas. O Celery requer um servidor Redis para funcionar
corretamente. Certifique-se de que o Redis esteja em execução (ou utilize `make start_redis` para iniciá-lo) antes de
utilizar o Celery.

### Iniciando o Celery Worker

Para iniciar um worker do Celery, execute o seguinte comando:

```bash
make start_celery
```

Isso iniciará um worker do Celery para processar tarefas assíncronas.

### Iniciando o Celery Beat

Para iniciar o Celery Beat, responsável por agendar tarefas, execute o seguinte comando:

```bash
make start_celery_beat
```

Isso iniciará o Celery Beat com o agendamento de tarefas especificado em seu projeto.

Lembre-se de que você deve executar o Celery Worker e o Celery Beat em instâncias separadas ou em terminais separados
para que o sistema de filas e agendamento funcione corretamente.

## Estrutura de Arquivos

O projeto possui um aplicativo chamado `commons`, além de algumas pastas auxiliares que compõem o projeto.
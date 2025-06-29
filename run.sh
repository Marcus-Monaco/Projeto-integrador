#!/bin/bash

# Script para executar o projeto Python
echo "=== Iniciando aplicação Python ==="

# Verificar se estamos na pasta correta
if [ ! -f "main.py" ]; then
    echo "Erro: Arquivo main.py não encontrado!"
    echo "Execute este script da pasta combo_python/"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Erro ao criar ambiente virtual!"
        exit 1
    fi
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se as dependências estão instaladas
echo "Verificando dependências..."
pip install -r requirements.txt

# Verificar se PostgreSQL está rodando
echo "Verificando PostgreSQL..."
if ! systemctl is-active --quiet postgresql; then
    echo "PostgreSQL não está rodando. Tentando iniciar..."
    sudo systemctl start postgresql
    if [ $? -ne 0 ]; then
        echo "Erro ao iniciar PostgreSQL!"
        echo "Execute: sudo systemctl start postgresql"
        exit 1
    fi
fi

# Perguntar qual banco de dados usar
echo "Escolha o banco de dados:"
echo "1) PostgreSQL (padrão)"
echo "2) MySQL"
read -p "Opção (1/2): " db_choice

# Configurar opção de banco de dados
if [ "$db_choice" = "2" ]; then
    DB_TYPE="mysql"
    
    # Verificar se MySQL está rodando
    echo "Verificando MySQL..."
    if ! systemctl is-active --quiet mysql; then
        echo "MySQL não está rodando. Tentando iniciar..."
        sudo systemctl start mysql
        if [ $? -ne 0 ]; then
            echo "Erro ao iniciar MySQL!"
            echo "Execute: sudo systemctl start mysql"
            exit 1
        fi
    fi
else
    DB_TYPE="postgresql"
fi

# Executar a aplicação
echo "Executando aplicação com banco de dados: $DB_TYPE..."
python main.py --db $DB_TYPE

# Verificar se houve erro
if [ $? -ne 0 ]; then
    echo "Erro ao executar a aplicação!"
    exit 1
fi

echo "=== Aplicação finalizada ==="

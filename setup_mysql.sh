#!/bin/bash

# Script para configurar o banco de dados MySQL
echo "=== Configurando banco de dados MySQL para o Sistema de Biblioteca ==="

# Verificar se MySQL está instalado
if ! command -v mysql &> /dev/null; then
    echo "MySQL não encontrado. Instalando..."
    sudo apt update
    sudo apt install mysql-server -y
    
    # Iniciar MySQL
    sudo systemctl start mysql
    sudo systemctl enable mysql
fi

# Verificar se MySQL está rodando
if ! systemctl is-active --quiet mysql; then
    echo "Iniciando MySQL..."
    sudo systemctl start mysql
    
    if [ $? -ne 0 ]; then
        echo "Erro ao iniciar MySQL!"
        exit 1
    fi
fi

# Criar banco de dados e usuário
echo "Criando banco de dados 'livros'..."

# Definir senha do root (se não estiver definida)
echo "Por favor, informe a senha do usuário root do MySQL (deixe em branco se não tiver senha):"
read -s MYSQL_ROOT_PASSWORD

# Criar banco e usuário
if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    # Sem senha
    sudo mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS livros;
CREATE USER IF NOT EXISTS 'biblioteca'@'localhost' IDENTIFIED BY 'biblioteca123';
GRANT ALL PRIVILEGES ON livros.* TO 'biblioteca'@'localhost';
FLUSH PRIVILEGES;
EOF
else
    # Com senha
    sudo mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<EOF
CREATE DATABASE IF NOT EXISTS livros;
CREATE USER IF NOT EXISTS 'biblioteca'@'localhost' IDENTIFIED BY 'biblioteca123';
GRANT ALL PRIVILEGES ON livros.* TO 'biblioteca'@'localhost';
FLUSH PRIVILEGES;
EOF
fi

# Verificar se o banco foi criado
if [ $? -ne 0 ]; then
    echo "Erro ao criar banco de dados MySQL!"
    exit 1
fi

echo "Banco de dados MySQL 'livros' criado com sucesso!"
echo "Usuário: biblioteca"
echo "Senha: biblioteca123"

# Criar tabelas e importar dados
echo "Criando tabelas..."

# Criar tabelas
cat <<EOF | mysql -u biblioteca -p'biblioteca123' livros
CREATE TABLE IF NOT EXISTS autor
(
  codigo numeric(10,0) NOT NULL,
  nome varchar(35) NOT NULL,
  PRIMARY KEY (codigo)
);

CREATE TABLE IF NOT EXISTS livros
(
  codigo numeric(10,0) NOT NULL,
  titulo varchar(45) NOT NULL,
  PRIMARY KEY (codigo)
);

CREATE TABLE IF NOT EXISTS edicao
(
  codigolivro numeric(10,0) NOT NULL,
  numero char(1) NOT NULL,
  ano int NOT NULL,
  PRIMARY KEY (codigolivro, numero),
  FOREIGN KEY (codigolivro) REFERENCES livros (codigo)
);

CREATE TABLE IF NOT EXISTS livroautor
(
  codigolivro numeric(10,0) NOT NULL,
  codigoautor numeric(10,0) NOT NULL,
  PRIMARY KEY (codigolivro, codigoautor),
  FOREIGN KEY (codigolivro) REFERENCES livros (codigo),
  FOREIGN KEY (codigoautor) REFERENCES autor (codigo)
);

CREATE TABLE IF NOT EXISTS livrostemp
(
  codigo numeric(10,0) NOT NULL,
  titulo varchar(45) NOT NULL,
  autor varchar(30) NOT NULL,
  edicao varchar(1) NOT NULL,
  ano int NOT NULL,
  PRIMARY KEY (codigo)
);
EOF

echo "Tabelas criadas com sucesso!"

# Importar dados dos scripts SQL
echo "Importando dados para o MySQL..."

# Função para remover configurações específicas do PostgreSQL e importar
import_sql_file() {
    local file=$1
    local temp_file=$(mktemp)
    
    echo "Processando $file..."
    
    # Remover configurações específicas do PostgreSQL
    grep -v "SET statement_timeout" "$file" | \
    grep -v "SET lock_timeout" | \
    grep -v "SET idle_in_transaction_session_timeout" | \
    grep -v "SET client_encoding" | \
    grep -v "SET standard_conforming_strings" | \
    grep -v "SELECT pg_catalog.set_config" | \
    grep -v "SET check_function_bodies" | \
    grep -v "SET xmloption" | \
    grep -v "SET client_min_messages" | \
    grep -v "SET row_security" | \
    grep -v "TOC entry" | \
    grep -v "Dependencies:" | \
    grep -v "Data for Name:" | \
    grep -v "Type: TABLE DATA" | \
    grep -v "Schema: public" | \
    grep -v "Owner: postgres" | \
    grep -v "^--" | \
    grep -v "^$" | \
    sed 's/INSERT INTO public\./INSERT INTO /g' > "$temp_file"
    
    # Importar para o MySQL
    mysql -u biblioteca -p'biblioteca123' livros < "$temp_file"
    
    # Verificar resultado
    if [ $? -eq 0 ]; then
        echo "✅ Importação de $file concluída com sucesso!"
    else
        echo "❌ Erro na importação de $file"
    fi
    
    # Remover arquivo temporário
    rm "$temp_file"
}

# Verificar se os arquivos SQL existem
SQL_DIR="sql_scripts"
if [ ! -d "$SQL_DIR" ]; then
    echo "❌ Diretório $SQL_DIR não encontrado!"
    exit 1
fi

# Importar os arquivos na ordem correta
echo "Importando dados dos livros..."
import_sql_file "$SQL_DIR/2 - livros.sql"

echo "Importando dados dos autores..."
import_sql_file "$SQL_DIR/3 - autor.sql"

echo "Importando dados das edições..."
import_sql_file "$SQL_DIR/4 - edicao.sql"

echo "Importando relacionamentos livro-autor..."
import_sql_file "$SQL_DIR/5 - livroautor.sql"

echo "Importando dados temporários..."
import_sql_file "$SQL_DIR/6 - livrostemp.sql"

# Verificar importação
echo "Verificando importação..."
mysql -u biblioteca -p'biblioteca123' livros -e "
SELECT 'Livros' AS 'Tabela', COUNT(*) AS 'Registros' FROM livros UNION
SELECT 'Autor', COUNT(*) FROM autor UNION
SELECT 'Edicao', COUNT(*) FROM edicao UNION
SELECT 'LivroAutor', COUNT(*) FROM livroautor UNION
SELECT 'LivrosTemp', COUNT(*) FROM livrostemp;
"

echo "=== Configuração do MySQL concluída! ==="
echo "Para executar o sistema com MySQL, use: ./run.sh e escolha a opção 2" 
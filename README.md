# 📚 Sistema de Biblioteca Python

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![Status](https://img.shields.io/badge/Status-Funcional-brightgreen.svg)

Um sistema de consulta de biblioteca com interface gráfica desenvolvido em Python, convertido de um projeto original em Java. Permite navegação e consulta de informações sobre livros armazenados em banco PostgreSQL.

## 🎯 Funcionalidades

- ✅ **Carregamento de Livros**: Visualiza 9.999 títulos em ComboBox
- ✅ **Consulta Detalhada**: Exibe livros, autores, edições e anos em tabela
- ✅ **Interface Intuitiva**: GUI moderna com Tkinter
- ✅ **Banco Robusto**: PostgreSQL com 5 tabelas interligadas (+30.000 registros)
- ✅ **Arquitetura MVC**: Padrão Model-View-Controller bem estruturado
- ✅ **Threading**: Operações assíncronas para melhor performance

## 📸 Preview

```
┌─────────────────────────────────────────────────┐
│           Sistema de Biblioteca Python          │
├─────────────────────────────────────────────────┤
│ Livro: [Dropdown com 9999 títulos ▼] [Carregar]│
│                                                 │
│ Livros e seus dados:              [Carregar]   │
│                                                 │
│                    [Fechar]                     │
└─────────────────────────────────────────────────┘
```

## 📋 Pré-requisitos

### Sistema Operacional
- **Linux** (Ubuntu/Debian - testado)
- **Python 3.8+**
- **PostgreSQL 12+**
- **Git**

### Verificar instalações
```bash
python3 --version  # Deve mostrar 3.8+
psql --version     # Deve mostrar 12+
git --version      # Qualquer versão recente
```

## 🚀 Instalação Completa

### 1. Clonar o repositório
```bash
# Clonar projeto
git clone https://github.com/Marcus-Monaco/Projeto-integrador.git
cd Projeto-integrador

# Verificar arquivos
ls -la
```

### 2. Instalar PostgreSQL (se necessário)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib python3-venv python3-pip

# Iniciar PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verificar se está rodando
sudo systemctl status postgresql
```

### 3. Configurar PostgreSQL
```bash
# Acessar como usuário postgres
sudo -u postgres psql

# Configurar senha do usuário postgres
\password postgres
# Digite: postgres (ou sua senha preferida)

# Sair
\q
```

### 4. Configurar ambiente Python
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

## 🗃️ Configuração do Banco de Dados

### 1. Criar banco de dados
```bash
# Criar banco 'livros'
sudo -u postgres createdb livros

# Verificar se foi criado
sudo -u postgres psql -l | grep livros
```

### 2. Executar scripts SQL (ORDEM IMPORTANTE!)

```bash
# Navegar para pasta dos scripts (se existir)
cd sql_scripts/ || echo "Pasta sql_scripts não encontrada - continue com o próximo passo"

# OU usar scripts da pasta raiz (ajuste conforme sua estrutura)
# Executar na ordem correta:

# 1. Criar tabelas
sudo -u postgres psql -d livros -f "1 - Criacao das tabelas"

# 2. Inserir livros
sudo -u postgres psql -d livros -f "2 - livros.sql"

# 3. Inserir autores  
sudo -u postgres psql -d livros -f "3 - autor.sql"

# 4. Inserir edições
sudo -u postgres psql -d livros -f "4 - edicao.sql"

# 5. Inserir relacionamentos livro-autor
sudo -u postgres psql -d livros -f "5 - livroautor.sql"

# 6. Inserir dados temporários
sudo -u postgres psql -d livros -f "6 - livrostemp.sql"
```

### 3. Validar importação
```bash
# Conectar ao banco
sudo -u postgres psql -d livros

# Executar validações (resultados esperados):
SELECT count(*) FROM livros;      -- Resultado: 9999
SELECT count(*) FROM autor;       -- Resultado: 9999  
SELECT count(*) FROM edicao;      -- Resultado: 11511
SELECT count(*) FROM livroautor;  -- Resultado: 10011
SELECT count(*) FROM livrostemp;  -- Resultado: 999

# Testar consulta completa
SELECT l.titulo, a.nome, e.numero, e.ano 
FROM livros l 
INNER JOIN livroautor la ON l.codigo = la.codigolivro 
INNER JOIN autor a ON a.codigo = la.codigoautor
INNER JOIN edicao e ON e.codigolivro = l.codigo 
LIMIT 5;

# Sair do psql
\q
```

## ▶️ Executando o Sistema

### Método 1: Script automatizado (Recomendado)
```bash
# Tornar script executável
chmod +x run.sh

# Executar
./run.sh
```

### Método 2: Execução manual
```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate

# Verificar dependências
pip install -r requirements.txt

# Executar aplicação
python main.py
```

### Método 3: Setup inicial completo
```bash
# Se for a primeira vez, execute o setup
chmod +x setup.sh
./setup.sh

# Depois execute normalmente
./run.sh
```

## 🖥️ Como Usar o Sistema

### Interface Principal

Quando executar o sistema, aparecerá uma janela com:

```
┌─────────────────────────────────────────────────┐
│           Sistema de Biblioteca Python          │
├─────────────────────────────────────────────────┤
│ Livro: [Lista suspensa vazia    ▼] [Carregar]  │
│                                                 │  
│ Livros e seus dados:               [Carregar]  │
│                                                 │
│                    [Fechar]                     │
└─────────────────────────────────────────────────┘
```

### 1. 📚 Carregar Lista de Livros

1. **Clique no primeiro botão "Carregar"** (ao lado do ComboBox)
2. **Aguarde** o carregamento (pode demorar alguns segundos)
3. **Popup aparecerá**: "Carregados 9999 registros!"
4. **ComboBox será populado** com todos os títulos de livros
5. **Navegue** pelos títulos usando a lista suspensa

### 2. 🔍 Consultar Dados Detalhados

1. **Clique no segundo botão "Carregar"** ("Livros e seus dados")
2. **Nova janela abrirá** com tabela contendo:
   - **Título** do livro
   - **Nome** do autor  
   - **Número** da edição
   - **Ano** de publicação
3. **Use as barras de rolagem** para navegar
4. **Double-click em qualquer linha** para selecionar
5. **Popup mostrará** os dados da linha selecionada
6. **Clique "Fechar"** para voltar à tela principal

### 3. 🚪 Fechar Sistema

- Clique em **"Fechar"** na tela principal
- Ou use o **X** da janela
- Confirmação aparecerá antes de fechar

## 📁 Estrutura do Projeto

```
Projeto-integrador/
├── 📂 database/              # 🔐 Camada de acesso ao banco
│   ├── dao_conectar_bd.py    # Conexão PostgreSQL
│   ├── dao_consultar_bd.py   # Execução de consultas  
│   ├── dao_string_conexao*.py # Configurações de conexão
│   └── exception_bd.py       # Tratamento de erros BD
│
├── 📂 business/              # 💼 Regras de negócio
│   ├── bo_combo.py          # Lógica do combo de livros
│   └── bo_conexao.py        # Gerenciamento de conexão
│
├── 📂 controllers/           # 🎮 Controladores (MVC)
│   ├── co_combo.py          # Controle da tela principal
│   └── co_consulta.py       # Controle da consulta
│
├── 📂 dao/                   # 🗃️ Data Access Objects
│   └── dao_combo.py         # Consultas específicas
│
├── 📂 gui/                   # 🖥️ Interface gráfica
│   ├── gui_combo.py         # Tela principal
│   └── 📂 consulta/
│       ├── gui_consulta.py   # Tela de consulta
│       └── gui_montar_table.py # Montagem de tabelas
│
├── 📂 models/                # 📊 Modelos de dados
│   └── vo_conexao.py        # Objeto de conexão
│
├── 📂 sql_scripts/           # 🗃️ Scripts do banco
│   ├── 0 - Instrucoes...     # Instruções
│   ├── 1 - Criacao das tabelas # DDL
│   ├── 2 - livros.sql       # Dados livros
│   ├── 3 - autor.sql        # Dados autores
│   ├── 4 - edicao.sql       # Dados edições
│   ├── 5 - livroautor.sql   # Relacionamentos
│   └── 6 - livrostemp.sql   # Dados temporários
│
├── 📄 .gitignore            # Arquivos ignorados
├── 📄 README.md             # Esta documentação
├── 📄 requirements.txt      # Dependências Python
├── 📄 setup.sh             # Script de configuração
├── 📄 run.sh               # Script de execução
└── 📄 main.py              # 🚀 Arquivo principal
```

## ⚙️ Configurações Avançadas

### Alterar configuração do banco
Edite `database/dao_string_conexao_postgresql.py`:

```python
def get_configuracao_alternativa(self):
    vo = VoConexao()
    vo.host = "localhost"        # Seu host
    vo.porta = "5432"           # Sua porta  
    vo.base_dados = "livros"    # Nome do banco
    vo.usuario = "postgres"     # Seu usuário
    vo.senha = "postgres"       # Sua senha
    return vo
```

### Executar com configurações customizadas
```bash
# Definir variáveis de ambiente
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=livros
export DB_USER=postgres
export DB_PASS=sua_senha

# Executar
python main.py
```

## 🐛 Troubleshooting

### ❌ Problema: "connection to server failed"
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Iniciar se parado
sudo systemctl start postgresql

# Reiniciar se necessário
sudo systemctl restart postgresql
```

### ❌ Problema: "ModuleNotFoundError: No module named 'psycopg2'"
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependência
pip install psycopg2-binary

# Ou instalar todas
pip install -r requirements.txt
```

### ❌ Problema: "database 'livros' does not exist"
```bash
# Criar banco novamente
sudo -u postgres createdb livros

# Verificar bancos existentes
sudo -u postgres psql -l
```

### ❌ Problema: Interface gráfica não abre
```bash
# Verificar DISPLAY (se usando SSH)
echo $DISPLAY

# Configurar se vazio
export DISPLAY=:0

# Instalar tkinter (se necessário)
sudo apt install python3-tkinter
```

### ❌ Problema: "Permission denied" no run.sh
```bash
# Dar permissão de execução
chmod +x run.sh
chmod +x setup.sh
```

### ❌ Problema: Dados não carregam
```bash
# Verificar se tabelas têm dados
sudo -u postgres psql -d livros -c "SELECT count(*) FROM livros;"

# Se retornar 0, executar scripts SQL novamente
```

### ❌ Problema: Pop-ups não aparecem
- Aguarde a operação terminar completamente
- Verifique se não há janelas minimizadas
- Reinicie a aplicação se necessário

## 📊 Dados do Sistema

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `livros` | 9.999 | Títulos dos livros |
| `autor` | 9.999 | Nomes dos autores |
| `edicao` | 11.511 | Edições e anos de publicação |
| `livroautor` | 10.011 | Relacionamento livro-autor |
| `livrostemp` | 999 | Dados temporários para testes |

**Total: ~42.000 registros**

## 🔄 Atualizações do Projeto

### Para desenvolvedores
```bash
# Fazer mudanças no código
# ...

# Commitar
git add .
git commit -m "feat: nova funcionalidade"
git push origin main
```

### Para usuários
```bash
# Atualizar projeto
git pull origin main

# Reinstalar dependências (se houve mudanças)
pip install -r requirements.txt
```

## 🎓 Sobre o Projeto

### Objetivo Educacional
Este sistema foi desenvolvido para fins educacionais, demonstrando:

- ✅ **Conversão Java → Python**: Migração completa de tecnologias
- ✅ **Padrões de Arquitetura**: MVC, DAO, BO
- ✅ **Conexão com Banco**: PostgreSQL com psycopg2
- ✅ **Interface Gráfica**: Tkinter (equivalente ao Swing)
- ✅ **Boas Práticas**: Estruturação, tratamento de erros, threading
- ✅ **Versionamento**: Git e GitHub

### Tecnologias Utilizadas
- **Python 3.8+**: Linguagem principal
- **Tkinter**: Interface gráfica
- **PostgreSQL**: Banco de dados
- **psycopg2**: Driver PostgreSQL
- **Threading**: Processamento assíncrono

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit suas mudanças: `git commit -m 'Adiciona nova feature'`
4. Push para a branch: `git push origin minha-feature`
5. Abra um Pull Request

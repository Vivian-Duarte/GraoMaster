# GrãoMaster - Guia de Instalação e Execução

Este guia contém o passo a passo para configurar o ambiente e rodar o script de povoamento do banco de dados.

## 1. Pré-requisitos (Instalação)

Instale os softwares abaixo (caso não tenha):

1.  **Python (3.10 ou superior)**
    * [Baixar Python](https://www.python.org/downloads/)
    *  **Importante:** Na instalação, marque a opção **"Add Python to PATH"**.
2.  **MongoDB Community Server** (O Banco de Dados)
    * [Baixar MongoDB Community](https://www.mongodb.com/try/download/community)
    * Instale como "Service" (padrão) para ele rodar automaticamente e coloque a opção **"Install MongoDB Compass"** .
3.  **MongoDB Compass** (Interface Visual)
    * Usado para ver os dados salvos. Geralmente instala junto com o Server.
4.  **Git**
    * Para baixar o projeto do repositório.

---

## 2. Configurando o Projeto

Siga estes passos no terminal (VS Code ou PowerShell):

### Passo 1: Criar o Ambiente Virtual
Digite: 

    python -m venv venv

### Passo 2: Ativar o Ambiente
Digite:

    .\venv\Scripts\activate

### Passo 3: Instalar as Dependências
Digite:

    pip install pymongo streamlit

### Passo 4: Criar e Povoar o Banco
### Para criar o banco GraoMasterDB e inserir os dados iniciais (Fazenda, Lote, Sacas):
    python scripts_banco.py

### Verificar os Dados (Visualmente)
1. Abra o MongoDB Compass.

2. Conecte em mongodb://localhost:27017.

3. Procure o banco GraoMasterDB na lista lateral.

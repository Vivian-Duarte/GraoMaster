# ☕ GrãoMaster - Guia de Instalação e Execução

Este guia contém o passo a passo para configurar o ambiente, visualizar os modelos, povoar o banco de dados e executar o Sistema de Banco de Dados (SBD) de rastreabilidade de cafés especiais.

---

## 1. Softwares Necessários (Pré-requisitos)

Certifique-se de ter os seguintes softwares instalados:

### Python (3.10 ou superior)
Durante a instalação no Windows, marque a opção **"Add Python to PATH"**.

### MongoDB Community Server
- Instale com as configurações padrão (**Run as a Service**).
- O MongoDB deve rodar na porta `27017`.
- A visualização dos dados deve ser feita exclusivamente pela interface do sistema (não utilizar Compass).

### Ferramentas de Modelagem (Opcional)
- **brModelo:** `Etapa_2\etapa_2_GraoMaster.brM3`
- **brModelo Next:** `Etapa_3\Etapa_3_alto_nivel.brm`

---

## 2. Configurando o Ambiente Python

Abra o terminal na pasta raiz do projeto e execute:

### Passo 1: Criar o ambiente virtual

```powershell
python -m venv venv
```

### Passo 2: Ativar o ambiente virtual

No Windows (PowerShell):

```powershell
.\venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

### Passo 3: Instalar dependências

```powershell
pip install pymongo
```

---

## 3. Executando o Sistema

Com o MongoDB rodando e o ambiente virtual ativado:

### Povoar o banco de dados

```powershell
python etapa_4_povoamento.py
```

### Abrir a interface gráfica

```powershell
python interface.py
```

---

## Observações

- Sempre ative o ambiente virtual antes de executar o sistema.
- Certifique-se de que o MongoDB esteja rodando.
- Caso ocorra erro de conexão, verifique se a porta `27017` está ativa.

---

Sistema GrãoMaster - Rastreabilidade de Cafés Especiais
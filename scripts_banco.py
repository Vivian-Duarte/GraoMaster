import pymongo
from datetime import datetime

# ------------------------------------------------------------------------------
# 1. CONEXÃO COM O BANCO DE DADOS
# ------------------------------------------------------------------------------
print("Conectando ao MongoDB...")
client = pymongo.MongoClient("mongodb://localhost:27017/") # Driver oficial Pymongo (Sem ORM)
db = client["GraoMasterDB"] # Criação do Banco NoSQL "GraoMasterDB"

# Limpeza para testes (Garante idempotência do script)
client.drop_database("GraoMasterDB")
print("Banco de dados limpo com sucesso! (Ambiente de Testes)")

# ------------------------------------------------------------------------------
# 2. DEFINIÇÃO DAS COLEÇÕES
# "Entidades principais: Fazenda, Talhão, Micro-lote, Processamento, Cupping e Saca"
# OBS: Em NoSQL, coleções são criadas dinamicamente, mas definimos as referências aqui.
# ------------------------------------------------------------------------------
col_fazendas = db["fazendas"]
col_talhoes = db["talhoes"]
col_lotes = db["microlotes"]
col_sacas = db["sacas"]

print("Iniciando povoamento...")

# ------------------------------------------------------------------------------
# 3. POVOAMENTO - FAZENDA E TALHÃO
# Aqui registramos a origem do café, incluindo fazenda, talhão...
# ------------------------------------------------------------------------------

# Criando FAZENDA
dados_fazenda = {
    "nome": "Fazenda Santa Clara",
    "proprietario": "João da Silva",
    "municipio": "Carmo de Minas",
    "regiao": "Mantiqueira de Minas"
}
id_fazenda = col_fazendas.insert_one(dados_fazenda).inserted_id
print(f"Fazenda criada. ID: {id_fazenda}")

# Criando TALHÃO (Vinculado à Fazenda)
dados_talhao = {
    "id_fazenda": id_fazenda,  # Referência ao Documento Pai (Fazenda)
    "identificacao": "Talhão do Sol",
    "altitude_media": 1250.0,
    "variedade_predominante": "Bourbon Amarelo"
}
id_talhao = col_talhoes.insert_one(dados_talhao).inserted_id
print(f"Talhão criado. ID: {id_talhao}")

# ------------------------------------------------------------------------------
# 4. POVOAMENTO - MICRO-LOTE (O CORAÇÃO DO SISTEMA)
# Utilizamos documentos incorporados para representar processos e avaliações
# Requisito de Negócio: Todo micro-lote deve conter informações obrigatórias de origem (altitude e variedade)
# ------------------------------------------------------------------------------

dados_lote = {
    "id_talhao": id_talhao, # Referência para Rastreabilidade da Origem
    "ano_colheita": 2025,
    
    # Campos altitude e variedade
    "altitude_real": 1260.0, 
    "variedade_real": "Bourbon Amarelo",
    
    "status": "Finalizado", # Controle de estado do lote

    # --- DOCUMENTOS EMBUTIDOS ---
    
    # Um micro-lote pode possuir múltiplos processos registrados, assim implementamos como uma lista de objetos dentro do documento do lote.
    "processamentos": [
        {
            "tipo": "Fermentação Anaeróbica",
            "data_inicio": datetime(2025, 6, 10),
            "data_fim": datetime(2025, 6, 12),
            "descricao": "Fermentação em tanque selado por 48h"
        }
    ],

    # Impossibilidade de finalizar um lote sem avaliação sensorial
    # Registrar avaliações sensoriais (Cupping protocolo SCA)
    # Objeto 'cupping' aninhado diretamente no lote
    "cupping": {
        "nota_sca": 88.5,
        "descritores": ["Frutas vermelhas", "Chocolate"],
        "data_avaliacao": datetime(2025, 8, 15),
        "qgrader": "Maria Especialista"
    }
}

id_lote = col_lotes.insert_one(dados_lote).inserted_id
print(f"Micro-lote criado com processos e cupping embutidos. ID: {id_lote}")

# ------------------------------------------------------------------------------
# 5. POVOAMENTO - SACAS (PRODUTO FINAL)
# Uma saca deve estar obrigatoriamente associada a um micro-lote válido e permitir a rastreabilidade até sua origem.
# ------------------------------------------------------------------------------

lista_sacas = [
    {
        "id_microlote": id_lote, # Chave Estrangeira (Referência) para o Lote
        "peso_kg": 60.0,
        "qrcode_rastreio": "SACA-001"
    },
    {
        "id_microlote": id_lote, # Várias sacas podem vir do mesmo lote (1:N)
        "peso_kg": 60.0,
        "qrcode_rastreio": "SACA-002"
    }
]

col_sacas.insert_many(lista_sacas)
print("Sacas criadas e vinculadas ao lote com sucesso.")

print("-" * 30)
print("Banco de dados criado e povoado")
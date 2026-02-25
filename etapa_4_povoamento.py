import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["GraoMaster"]

fazendas_col = db["fazendas"]
microlotes_col = db["microlotes"]
sacas_col = db["sacas"]

fazendas_col.drop()
microlotes_col.drop()
sacas_col.drop()

print("Inserindo dados no MongoDB pelo Python...\n")

fazenda = {
    "_id": "sitio_do_sol_001",
    "Nome": "Sítio do Sol",
    "Conformidade_Certificacao": {
        "Safra_Avaliada": 2026,
        "Responsabilidade_Economica": "Aprovado",
        "Condicoes_Sociais": "Aprovado",
        "Impactos_Ambientais": "Aprovado"
    }
}
fazendas_col.insert_one(fazenda)

microlote = {
    "_id": "LOTE-001",
    "Ano_safra": 2026,
    "Status": "Finalizado - Certificado",
    "Talhao": "Encosta Sul",
    "ID_fazenda": "sitio_do_sol_001",
    "Origem": {
        "Altitude_Metros": 1200.5,
        "Variedade_Planta": "Bourbon Amarelo"
    },
    "Avaliacao_Sensorial": {
        "Nota_sca": 85.5,                  
        "Avaliador": "Dona Sônia",         
        "Descricao": "Rapadura e Frutas",  
        "Realizada": True
    }
}
microlotes_col.insert_one(microlote)

saca = {
    "_id": "SACA-001",
    "Peso_kg": 60.0,           
    "Status_Saca": "Pronta",
    "id_lote": "LOTE-001"      
}
sacas_col.insert_one(saca)

print("--- RESULTADO DA CONSULTA DE RASTREABILIDADE ---")
lote_salvo = microlotes_col.find_one({"_id": "LOTE-001"})
fazenda_salva = fazendas_col.find_one({"_id": lote_salvo["ID_fazenda"]})
saca_salva = sacas_col.find_one({"id_lote": lote_salvo["_id"]})

print(f"Fazenda Cadastrada: {fazenda_salva['Nome']} (ID: {fazenda_salva['_id']})")
print(f"Lote Encontrado: {lote_salvo['_id']} | Nota SCA: {lote_salvo['Avaliacao_Sensorial']['Nota_sca']}")
print(f"Saca Gerada: {saca_salva['_id']} | Peso: {saca_salva['Peso_kg']}kg")
print(f"Auditoria da Origem: Impactos Ambientais -> {fazenda_salva['Conformidade_Certificacao']['Impactos_Ambientais']}")
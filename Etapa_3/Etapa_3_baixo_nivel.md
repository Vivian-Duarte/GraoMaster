# Projeto Lógico de Baixo Nível (Esquema Físico MongoDB)

Para o mapeamento conceitual-lógico de baixo nível, adotamos a representação do esquema JSON das coleções, refletindo a abordagem híbrida adequada para bancos orientados a documentos.

## 1. Coleção: Fazendas
Armazena os dados da propriedade e embute a auditoria de certificação.

```json
{
  "_id": "String (PK)",
  "Nome": "String",
  "Conformidade_Certificacao": {
    "Safra_Avaliada": "Integer",
    "Responsabilidade_Economica": "String",
    "Condicoes_Sociais": "String",
    "Impactos_Ambientais": "String"
  }
}
```

## 2. Coleção: Microlotes
Referencia a fazenda de origem (1:N) e embute os dados de Origem e laudo sensorial (Cupping).

```json
{
  "_id": "String (PK)",
  "Ano_safra": "Integer",
  "Status": "String",
  "Talhao": "String",
  "ID_fazenda": "String (FK -> Ref: Fazendas._id)",
  "Origem": {
    "Altitude_Metros": "Float",
    "Variedade_Planta": "String"
  },
  "Avaliacao_Sensorial": {
    "Nota_sca": "Float",
    "Avaliador": "String",
    "Descricao": "String",
    "Realizada": "Boolean"
  }
}
```

## 3. Coleção: Sacas
Referencia o microlote (1:N), pois representam unidades físicas de alto volume que serão rastreadas individualmente.

```json
{
  "_id": "String (PK)",
  "Peso_kg": "Float",
  "Status_Saca": "String",
  "id_lote": "String (FK -> Ref: Microlotes._id)"
}
```
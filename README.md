# CoffeeTrace: Rastreabilidade de Cafés Especiais

**Universidade Federal de Ouro Preto (UFOP)**  
**ICEA – Departamento de Computação e Sistemas (DECSI)**  
**Disciplina:** CS1603 – Banco de Dados II  

**Desenvolvimento:**  
Vívian Evelyn Duarte – 23.2.8017

Nicholas Arthur Guimarães Andrade – 23.2.8018 

---

##  1. Sobre o Projeto

O **CoffeeTrace** é um Sistema de Banco de Dados (SBD) não relacional desenvolvido com o objetivo de realizar a rastreabilidade completa de micro-lotes de cafés especiais, acompanhando o produto desde sua origem na fazenda e no talhão até a saca final comercializada.

### Contexto e Motivação

A rastreabilidade é um fator essencial no mercado de cafés especiais, pois características como origem, variedade da planta, altitude e método de processamento impactam diretamente a qualidade percebida e o valor comercial do produto.  

A ausência de um registro estruturado e confiável dessas informações pode resultar em perda de valor, dificuldades de certificação e menor transparência para compradores e consumidores finais. Nesse contexto, o CoffeeTrace surge como uma solução para organizar e manter essas informações de forma flexível e consistente.

---

##  2. Objetivos do Projeto

### Objetivo Geral

Desenvolver um sistema de rastreabilidade de micro-lotes de cafés especiais utilizando um banco de dados NoSQL.

### Objetivos Específicos

- Registrar a origem do café, incluindo fazenda, talhão, altitude e variedade;
- Registrar diferentes processos de beneficiamento e secagem;
- Registrar avaliações sensoriais (Cupping – protocolo SCA);
- Garantir regras de negócio, como a impossibilidade de finalizar um lote sem avaliação sensorial;
- Permitir a rastreabilidade de sacas até sua origem por meio de uma interface dedicada.

---

##  3. Justificativa do Uso de Banco de Dados NoSQL

A escolha por um Sistema Gerenciador de Banco de Dados não relacional (NoSQL) justifica-se pelas características do domínio do problema:

- **Flexibilidade de esquema:** Micro-lotes podem possuir estruturas distintas, uma vez que diferentes métodos de processamento (via seca, via úmida, fermentação, entre outros) demandam atributos específicos;
- **Modelo de documentos:** O uso de documentos permite a evolução do esquema sem interrupções no sistema, além de reduzir a complexidade de junções quando comparado a modelos relacionais tradicionais;
- **Adequação ao domínio:** A modelagem orientada a documentos representa de forma natural a hierarquia e a variabilidade dos dados envolvidos na rastreabilidade do café.

---

##  4. Arquitetura do Sistema

O sistema foi desenvolvido respeitando rigorosamente as restrições estabelecidas pela disciplina:

- **Interface do Usuário:** Implementada em Python (Web ou Desktop), garantindo que não haja interação por linha de comando;
- **Comunicação com o Banco de Dados:** Realizada exclusivamente por meio do driver oficial do SGBD, sem utilização de ORM (Object-Relational Mapping) ou bibliotecas que abstraiam as operações de acesso aos dados;
- **Banco de Dados:** MongoDB, um SGBD NoSQL orientado a documentos.

---

##  5. Modelagem dos Dados

A modelagem do sistema segue as etapas de projeto conceitual e lógico exigidas no contexto acadêmico:

- **Entidades principais:** Fazenda, Talhão, Micro-lote, Processamento, Cupping e Saca;
- **Abordagem de modelagem:** Utilização de documentos incorporados para representar processos e avaliações sensoriais, e referências para garantir a rastreabilidade de longo alcance entre sacas e micro-lotes;
- **Objetivo da modelagem:** Otimizar consultas de rastreabilidade e reduzir a complexidade estrutural dos dados.

---

##  6. Regras de Negócio Implementadas

O sistema garante as seguintes regras de negócio:

- Um micro-lote não pode ser finalizado sem a realização da avaliação sensorial (Cupping);
- Todo micro-lote deve conter informações obrigatórias de origem, incluindo altitude e variedade;
- Um micro-lote pode possuir múltiplos processos registrados;
- Uma saca deve estar obrigatoriamente associada a um micro-lote válido.

---

##  7. Funcionalidades do Sistema

O sistema permite, por meio de sua interface, as seguintes funcionalidades:

- **Cadastro:** Micro-lotes, processos de beneficiamento e sacas;
- **Avaliação:** Registro de notas sensoriais segundo o protocolo SCA (Cupping);
- **Gestão:** Finalização de micro-lotes e listagem de lotes pendentes;
- **Consulta:** Rastreabilidade completa da saca até a origem no talhão.

---

##  Observações Acadêmicas

Este projeto foi desenvolvido exclusivamente para fins acadêmicos, como parte das atividades da disciplina **CS1603 – Banco de Dados II**, não possuindo finalidade comercial.

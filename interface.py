import tkinter as tk
from tkinter import ttk, messagebox
import pymongo
import unicodedata
import re

try:
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info() 
    db = client["GraoMaster"]
    microlotes_col = db["microlotes"]
    fazendas_col = db["fazendas"]
    sacas_col = db["sacas"]
except pymongo.errors.ServerSelectionTimeoutError:
    print("ERRO CRÍTICO: Não foi possível conectar ao MongoDB.")

def limpar_nome_para_id(nome):

    nfkd = unicodedata.normalize('NFKD', nome)
    nome_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    id_limpo = re.sub(r'[^a-zA-Z0-9]', '_', nome_sem_acento).lower()
    id_limpo = re.sub(r'_+', '_', id_limpo).strip('_')
    return id_limpo

def cadastrar_origem(event=None):

    nome_fazenda = entry_fazenda_prod.get().strip()
    id_lote = entry_lote_prod.get().strip().upper()
    safra_str = entry_safra_prod.get().strip()
    talhao = entry_talhao_prod.get().strip()
    altitude = entry_alt_prod.get().strip()
    variedade = entry_var_prod.get().strip()

    if not all([nome_fazenda, id_lote, safra_str, talhao, altitude, variedade]):
        messagebox.showwarning("Aviso", "Todos os campos de origem são obrigatórios!")
        return

    try:
        safra = int(safra_str)
        if safra > 2026:
            messagebox.showerror("Erro de Validação", "O Ano da Safra não pode ser maior do que 2026!")
            entry_safra_prod.focus()
            return
    except ValueError:
        messagebox.showerror("Erro", "O Ano da Safra deve ser um número válido (Ex: 2025).")
        return

    fazenda_existente = fazendas_col.find_one({"Nome": {"$regex": f"^{nome_fazenda}$", "$options": "i"}})
    
    if fazenda_existente:
        id_fazenda = fazenda_existente["_id"]
    else:
        string_limpa = limpar_nome_para_id(nome_fazenda)
        id_fazenda = f"{string_limpa}_001"

        fazendas_col.insert_one({
            "_id": id_fazenda, 
            "Nome": nome_fazenda,
            "Conformidade_Certificacao": {
                "Safra_Avaliada": safra,
                "Responsabilidade_Economica": "Pendente",
                "Condicoes_Sociais": "Pendente",
                "Impactos_Ambientais": "Pendente"
            }
        })

    novo_lote = {
        "_id": id_lote,
        "ID_fazenda": id_fazenda,
        "Ano_safra": safra,
        "Status": "Pendente", 
        "Talhao": talhao,
        "Origem": {
            "Altitude_Metros": float(altitude), 
            "Variedade_Planta": variedade
        },
        "Avaliacao_Sensorial": {
            "Realizada": False
        }
    }
    
    try:
        microlotes_col.insert_one(novo_lote)
        messagebox.showinfo("Sucesso", f"Lote {id_lote} cadastrado!\nVinculado à fazenda: {nome_fazenda} (ID: {id_fazenda})")
        entry_fazenda_prod.delete(0, tk.END); entry_lote_prod.delete(0, tk.END); entry_safra_prod.delete(0, tk.END)
        entry_talhao_prod.delete(0, tk.END); entry_alt_prod.delete(0, tk.END); entry_var_prod.delete(0, tk.END)
        entry_fazenda_prod.focus()
    except pymongo.errors.DuplicateKeyError:
        messagebox.showerror("Erro", "Este Código de Lote já existe!")

def buscar_lote_avaliador(event=None):
    id_busca = entry_busca_aval.get().strip().upper() 
    if not id_busca: return
    
    lote = microlotes_col.find_one({"_id": id_busca})
    if not lote:
        messagebox.showerror("Erro", "Lote não encontrado no sistema.")
        return
    if "Finalizado" in lote.get("Status", ""):
        messagebox.showinfo("Aviso", "Este lote já foi avaliado e finalizado.")
        return

    lbl_id_lote_destaque.config(text=f"LOTE SELECIONADO: {lote['_id']}")
    var_econ.set("Reprovado"); var_soc.set("Reprovado"); var_amb.set("Reprovado")
    entry_nota_aval.delete(0, tk.END); entry_desc_aval.delete(0, tk.END); entry_nome_aval.delete(0, tk.END)
    frame_formulario_aval.pack(fill="both", expand=True, padx=10, pady=5)
    entry_nota_aval.focus()

def salvar_auditoria_cupping(event=None):
    id_lote = entry_busca_aval.get().strip().upper() 
    nota = entry_nota_aval.get().strip()
    descricao = entry_desc_aval.get().strip()
    avaliador = entry_nome_aval.get().strip()

    if not all([id_lote, nota, descricao, avaliador]):
        messagebox.showwarning("Aviso", "Preencha a Nota SCA, Descrição e Nome do Avaliador.")
        return

    if var_econ.get() == "Aprovado" and var_soc.get() == "Aprovado" and var_amb.get() == "Aprovado":
        status_final = "Finalizado - Certificado"
    else:
        status_final = "Finalizado - Não Conforme"

    lote = microlotes_col.find_one({"_id": id_lote})
    
    fazendas_col.update_one(
        {"_id": lote["ID_fazenda"]},
        {"$set": {
            "Conformidade_Certificacao.Safra_Avaliada": lote["Ano_safra"],
            "Conformidade_Certificacao.Responsabilidade_Economica": var_econ.get(),
            "Conformidade_Certificacao.Condicoes_Sociais": var_soc.get(),
            "Conformidade_Certificacao.Impactos_Ambientais": var_amb.get()
        }}
    )

    microlotes_col.update_one(
        {"_id": id_lote},
        {"$set": {
            "Status": status_final, 
            "Avaliacao_Sensorial": {
                "Realizada": True,
                "Nota_sca": float(nota.replace(',', '.')),
                "Avaliador": avaliador,
                "Descricao": descricao
            }
        }}
    )

    messagebox.showinfo("Sucesso", f"Lote salvo! Status Final: {status_final}")
    frame_formulario_aval.pack_forget()
    entry_busca_aval.delete(0, tk.END)
    lbl_id_lote_destaque.config(text="")


def atualizar_lotes_ensaque(event=None):
    lotes_finalizados = microlotes_col.find({"Status": {"$regex": "^Finalizado"}})
    lista_lotes = [lote["_id"] for lote in lotes_finalizados]
    
    if lista_lotes:
        combo_lote_ensaque['values'] = lista_lotes
    else:
        combo_lote_ensaque['values'] = ["Nenhum lote finalizado"]
        combo_lote_ensaque.set("Nenhum lote finalizado")

def ensacar_lote(event=None):
    id_lote = combo_lote_ensaque.get().strip() 
    id_saca = entry_saca_ensaque.get().strip().upper() 
    peso = entry_peso_ensaque.get().strip()

    if not all([id_saca, id_lote, peso]) or id_lote == "Nenhum lote finalizado":
        messagebox.showwarning("Aviso", "Preencha todos os campos da Saca corretamente.")
        return

    lote = microlotes_col.find_one({"_id": id_lote})
    if not lote or not lote.get("Status", "").startswith("Finalizado"):
        messagebox.showerror("Acesso Negado", "Apenas lotes FINALIZADOS podem ser ensacados!")
        return

    try:
        sacas_col.insert_one({"_id": id_saca, "id_lote": id_lote, "Peso_kg": float(peso), "Status_Saca": "Pronta"})
        messagebox.showinfo("Sucesso", f"Saca {id_saca} registrada!")
        combo_lote_ensaque.set(''); entry_saca_ensaque.delete(0, tk.END); entry_peso_ensaque.delete(0, tk.END)
        combo_lote_ensaque.focus()
    except pymongo.errors.DuplicateKeyError:
        messagebox.showerror("Erro", "Este ID de Saca já está cadastrado!")

def buscar_rastreabilidade(event=None):
    id_saca = entry_busca.get().strip().upper() 
    if not id_saca: return

    pipeline = [
        {"$match": {"_id": id_saca}},
        {"$lookup": {"from": "microlotes", "localField": "id_lote", "foreignField": "_id", "as": "dados_lote"}},
        {"$unwind": "$dados_lote"},
        {"$lookup": {"from": "fazendas", "localField": "dados_lote.ID_fazenda", "foreignField": "_id", "as": "dados_fazenda"}},
        {"$unwind": {"path": "$dados_fazenda", "preserveNullAndEmptyArrays": True}}
    ]
    
    res = list(sacas_col.aggregate(pipeline))
    
    text_resultado.config(state=tk.NORMAL)
    text_resultado.delete(1.0, tk.END)

    if not res:
        text_resultado.insert(tk.END, "Saca não encontrada no sistema.\n", "center")
        text_resultado.config(state=tk.DISABLED)
        return

    saca = res[0]
    lote = saca["dados_lote"]
    fazenda = saca.get("dados_fazenda", {})
    pilares = fazenda.get("Conformidade_Certificacao", {})

    if lote.get("Status") == "Finalizado - Não Conforme":
        reprovados = []
        if pilares.get('Responsabilidade_Economica') == 'Reprovado': reprovados.append("Responsabilidade Econômica")
        if pilares.get('Condicoes_Sociais') == 'Reprovado': reprovados.append("Condições Sociais")
        if pilares.get('Impactos_Ambientais') == 'Reprovado': reprovados.append("Impactos Ambientais")
        
        pilares_str = ", ".join(reprovados)
        nome_faz = fazenda.get('Nome', 'Desconhecida')
        
        text_resultado.insert(tk.END, f" ATENÇÃO: Este lote possui Não Conformidade na origem.\n\n", ("alerta_vermelho", "center"))
        text_resultado.insert(tk.END, f"Auditoria: A fazenda {nome_faz} foi avaliada e REPROVADA em [{pilares_str}] nesta safra.\n", ("alerta_vermelho", "center"))
        text_resultado.insert(tk.END, "-"*65 + "\n\n", "center")

    saida = f"=== RASTREABILIDADE DA SACA: {saca['_id']} ===\n\n"
    
    saida += f"[DADOS DA SACA]\n"
    saida += f"ID da Saca: {saca['_id']} | Peso: {saca.get('Peso_kg')} kg\n"
    saida += f"Status: {lote.get('Status').upper()}\n\n"

    saida += f"[PERFIL DO LOTE E AVALIAÇÃO]\n"
    saida += f"Veio do Lote: {lote['_id']} | Safra: {lote.get('Ano_safra')}\n"
    saida += f"Nota SCA: {lote['Avaliacao_Sensorial'].get('Nota_sca')} | Descrição: {lote['Avaliacao_Sensorial'].get('Descricao', 'N/A')}\n"
    saida += f"Avaliador Responsável: {lote['Avaliacao_Sensorial'].get('Avaliador', 'N/A')}\n\n"

    saida += f"[ ORIGEM E TERROIR]\n"
    saida += f"Fazenda: {fazenda.get('Nome', 'Não informada')} (ID: {lote.get('ID_fazenda')})\n"
    saida += f"Talhão: {lote.get('Talhao', 'N/A')}\n"
    saida += f"Variedade: {lote.get('Origem', {}).get('Variedade_Planta', 'N/A')} | Altitude: {lote.get('Origem', {}).get('Altitude_Metros', 'N/A')}m\n\n"

    text_resultado.insert(tk.END, saida, "center")
    text_resultado.config(state=tk.DISABLED)

janela = tk.Tk()
janela.title("GrãoMaster - Sistema Completo de Rastreabilidade")
janela.geometry("650x780") 

fonte_titulo = ("Arial", 18, "bold")
fonte_label = ("Arial", 11, "bold") 
fonte_desc = ("Arial", 9)
cor_desc = "#555555"
cor_primaria = "#FF9800" 

abas = ttk.Notebook(janela)
abas.pack(pady=10, expand=True, fill="both")

aba_produtor = ttk.Frame(abas)
abas.add(aba_produtor, text=" 1. Produtor")

tk.Label(aba_produtor, text="Cadastrar Origem do Lote", font=fonte_titulo, fg=cor_primaria).pack(pady=(15, 10))

tk.Label(aba_produtor, text="Nome da Fazenda", font=fonte_label).pack()
tk.Label(aba_produtor, text="(Ex: Sítio do Sol)", font=fonte_desc, fg=cor_desc).pack()
entry_fazenda_prod = tk.Entry(aba_produtor, width=40); entry_fazenda_prod.pack(pady=(0, 10))

tk.Label(aba_produtor, text="Código do Lote", font=fonte_label).pack()
tk.Label(aba_produtor, text="(Ex: Lote-001)", font=fonte_desc, fg=cor_desc).pack()
entry_lote_prod = tk.Entry(aba_produtor, width=40); entry_lote_prod.pack(pady=(0, 10))

tk.Label(aba_produtor, text="Ano da Safra", font=fonte_label).pack()
tk.Label(aba_produtor, text="(Ex: 2025)", font=fonte_desc, fg=cor_desc).pack()
entry_safra_prod = tk.Entry(aba_produtor, width=40); entry_safra_prod.pack(pady=(0, 10))

tk.Label(aba_produtor, text="Talhão", font=fonte_label).pack()
entry_talhao_prod = tk.Entry(aba_produtor, width=40); entry_talhao_prod.pack(pady=(0, 10))

tk.Label(aba_produtor, text="Altitude", font=fonte_label).pack()
tk.Label(aba_produtor, text="(Em metros)", font=fonte_desc, fg=cor_desc).pack()
entry_alt_prod = tk.Entry(aba_produtor, width=40); entry_alt_prod.pack(pady=(0, 10))

tk.Label(aba_produtor, text="Variedade", font=fonte_label).pack()
tk.Label(aba_produtor, text="(Tipo do seu café)", font=fonte_desc, fg=cor_desc).pack()
entry_var_prod = tk.Entry(aba_produtor, width=40); entry_var_prod.pack(pady=(0, 15))

tk.Button(aba_produtor, text="Salvar Lote Pendente", font=("Arial", 11, "bold"), command=cadastrar_origem, bg=cor_primaria, fg="white", padx=10, pady=5).pack()

entry_fazenda_prod.bind("<Return>", lambda e: entry_lote_prod.focus())
entry_lote_prod.bind("<Return>", lambda e: entry_safra_prod.focus())
entry_safra_prod.bind("<Return>", lambda e: entry_talhao_prod.focus())
entry_talhao_prod.bind("<Return>", lambda e: entry_alt_prod.focus())
entry_alt_prod.bind("<Return>", lambda e: entry_var_prod.focus())
entry_var_prod.bind("<Return>", cadastrar_origem)
entry_fazenda_prod.focus()

aba_avaliador = ttk.Frame(abas)
abas.add(aba_avaliador, text=" 2. Avaliador / Auditor")

frame_busca = tk.Frame(aba_avaliador)
frame_busca.pack(pady=10)
tk.Label(frame_busca, text="Buscar ID do Lote Pendente:").pack(side=tk.LEFT, padx=5)
entry_busca_aval = tk.Entry(frame_busca, width=20); entry_busca_aval.pack(side=tk.LEFT, padx=5)
tk.Button(frame_busca, text="Buscar", command=buscar_lote_avaliador, bg="#2196F3", fg="white").pack(side=tk.LEFT)
entry_busca_aval.bind("<Return>", buscar_lote_avaliador)

lbl_id_lote_destaque = tk.Label(aba_avaliador, text="", font=fonte_titulo, fg=cor_primaria)
lbl_id_lote_destaque.pack(pady=5)

frame_formulario_aval = tk.Frame(aba_avaliador)
var_econ = tk.StringVar(value="Reprovado"); var_soc = tk.StringVar(value="Reprovado"); var_amb = tk.StringVar(value="Reprovado")

frame_pilares = tk.LabelFrame(frame_formulario_aval, text="Verificação de Pilares (Auditoria Fazenda)", font=("Arial", 12, "bold"), padx=10, pady=10)
frame_pilares.pack(fill="x", pady=5)

tk.Label(frame_pilares, text="Responsabilidade Econômica:", font=fonte_label).pack(anchor="w")
tk.Label(frame_pilares, text="Avalia a gestão transparente dos recursos, a rastreabilidade das operações financeiras e as práticas de comércio justo com fornecedores e colaboradores.", font=fonte_desc, fg=cor_desc, wraplength=580, justify="left").pack(anchor="w")
frame_rad1 = tk.Frame(frame_pilares); frame_rad1.pack(anchor="w", pady=2)
tk.Radiobutton(frame_rad1, text="Aprovado", variable=var_econ, value="Aprovado").pack(side=tk.LEFT)
tk.Radiobutton(frame_rad1, text="Reprovado", variable=var_econ, value="Reprovado").pack(side=tk.LEFT)

tk.Label(frame_pilares, text="Condições Sociais:", font=fonte_label).pack(anchor="w", pady=(10, 0))
tk.Label(frame_pilares, text="Garante o respeito rigoroso às leis trabalhistas, exigência do uso de EPIs, condições seguras de trabalho e o bem-estar geral na propriedade.", font=fonte_desc, fg=cor_desc, wraplength=580, justify="left").pack(anchor="w")
frame_rad2 = tk.Frame(frame_pilares); frame_rad2.pack(anchor="w", pady=2)
tk.Radiobutton(frame_rad2, text="Aprovado", variable=var_soc, value="Aprovado").pack(side=tk.LEFT)
tk.Radiobutton(frame_rad2, text="Reprovado", variable=var_soc, value="Reprovado").pack(side=tk.LEFT)

tk.Label(frame_pilares, text="Impactos Ambientais:", font=fonte_label).pack(anchor="w", pady=(10, 0))
tk.Label(frame_pilares, text="Monitora a preservação de nascentes e APPs, controle rigoroso de desmatamento, uso racional de água e o descarte correto de resíduos e embalagens.", font=fonte_desc, fg=cor_desc, wraplength=580, justify="left").pack(anchor="w")
frame_rad3 = tk.Frame(frame_pilares); frame_rad3.pack(anchor="w", pady=2)
tk.Radiobutton(frame_rad3, text="Aprovado", variable=var_amb, value="Aprovado").pack(side=tk.LEFT)
tk.Radiobutton(frame_rad3, text="Reprovado", variable=var_amb, value="Reprovado").pack(side=tk.LEFT)

frame_cupping = tk.LabelFrame(frame_formulario_aval, text="Avaliação Sensorial (Cupping)", font=("Arial", 12, "bold"), padx=10, pady=10)
frame_cupping.pack(fill="x", pady=5)
tk.Label(frame_cupping, text="Nota SCA:").pack(anchor="w"); entry_nota_aval = tk.Entry(frame_cupping, width=40); entry_nota_aval.pack(anchor="w", pady=(0, 5))
tk.Label(frame_cupping, text="Descrição do Café:").pack(anchor="w"); entry_desc_aval = tk.Entry(frame_cupping, width=40); entry_desc_aval.pack(anchor="w", pady=(0, 5))
tk.Label(frame_cupping, text="Avaliador/Auditor:").pack(anchor="w"); entry_nome_aval = tk.Entry(frame_cupping, width=40); entry_nome_aval.pack(anchor="w", pady=(0, 5))

tk.Button(frame_formulario_aval, text=" Salvar Auditoria e Finalizar Lote", command=salvar_auditoria_cupping, bg=cor_primaria, fg="white", font=("Arial", 11, "bold")).pack(pady=15)

aba_ensaque = ttk.Frame(abas)
abas.add(aba_ensaque, text=" 3. Ensacamento")
tk.Label(aba_ensaque, text="Gerar Sacas do Lote Finalizado", font=fonte_titulo, fg=cor_primaria).pack(pady=10)

tk.Label(aba_ensaque, text="ID Lote de Origem:", font=fonte_label).pack()
combo_lote_ensaque = ttk.Combobox(aba_ensaque, width=38, state="readonly")
combo_lote_ensaque.pack(pady=(0, 10))
combo_lote_ensaque.bind("<Button-1>", atualizar_lotes_ensaque) 

tk.Label(aba_ensaque, text="ID Saca (Ex: SACA-001):", font=fonte_label).pack()
entry_saca_ensaque = tk.Entry(aba_ensaque, width=40)
entry_saca_ensaque.pack(pady=(0, 10))

tk.Label(aba_ensaque, text="Peso (kg):", font=fonte_label).pack()
entry_peso_ensaque = tk.Entry(aba_ensaque, width=40)
entry_peso_ensaque.pack(pady=(0, 10))

tk.Button(aba_ensaque, text="Registrar Saca", command=ensacar_lote, bg="#795548", fg="white", font=("Arial", 11, "bold")).pack(pady=15)

combo_lote_ensaque.bind("<Return>", lambda e: entry_saca_ensaque.focus())
entry_saca_ensaque.bind("<Return>", lambda e: entry_peso_ensaque.focus())
entry_peso_ensaque.bind("<Return>", ensacar_lote)

aba_rastreio = ttk.Frame(abas)
abas.add(aba_rastreio, text=" 4. Rastreabilidade")
tk.Label(aba_rastreio, text="Rastreabilidade da Saca", font=fonte_titulo, fg=cor_primaria).pack(pady=10)
tk.Label(aba_rastreio, text="Digite o ID da SACA:").pack(); entry_busca = tk.Entry(aba_rastreio, width=40); entry_busca.pack()
tk.Button(aba_rastreio, text="Buscar", command=buscar_rastreabilidade, bg="#2196F3", fg="white").pack(pady=10)
entry_busca.bind("<Return>", buscar_rastreabilidade)

text_resultado = tk.Text(aba_rastreio, height=22, width=70, bg="#2b2b2b", fg="#a9b7c6", font=("Consolas", 10))
text_resultado.tag_config("alerta_vermelho", foreground="#ff4d4d", font=("Consolas", 10, "bold"))
text_resultado.tag_configure("center", justify="center") 
text_resultado.pack(pady=10)

janela.mainloop()

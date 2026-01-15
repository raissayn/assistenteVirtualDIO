import streamlit as st
import pandas as pd
import json
import os
import requests

# ==============================================================================
# 0. CONFIGURAÇÃO (Ollama URL & Modelo)
# ==============================================================================
OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO_PADRAO = "llama3:8b"

st.set_page_config(page_title="Edu - AI Financeiro", page_icon="💰", layout="wide")

def setup_dados_iniciais():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists("data/transacoes.csv"):
        csv_data = """data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Aluguel,moradia,1200.00,saida
2025-10-15,Luz,moradia,150.00,saida
2025-10-20,Ifood,alimentacao,80.00,saida
2025-10-25,Uber,transporte,200.00,saida"""
        with open("data/transacoes.csv", "w", encoding='utf-8') as f:
            f.write(csv_data)

    if not os.path.exists("data/perfil_investidor.json"):
        with open("data/perfil_investidor.json", "w", encoding='utf-8') as f:
            json.dump({"nome": "Raissa", "perfil_investidor": "moderado", "aceita_risco": False, "objetivo_principal": "Reserva"}, f)
    
    if not os.path.exists("data/produtos_financeiros.json"):
        with open("data/produtos_financeiros.json", "w", encoding='utf-8') as f:
            json.dump([{"nome": "Tesouro Selic", "rentabilidade": "15% a.a.", "risco": "baixo"}], f)

setup_dados_iniciais()

# ==============================================================================
# 1. CARREGA DADOS E PROCESSA CATEGORIAS
# ==============================================================================
try:
    perfil = json.load(open('data/perfil_investidor.json', encoding='utf-8'))
    produtos = json.load(open('data/produtos_financeiros.json', encoding='utf-8'))
    transacoes = pd.read_csv('data/transacoes.csv')
except Exception as e:
    st.error(f"Erro ao carregar arquivos: {e}")
    st.stop()
    
# Cálculos de Totais
total_entradas = transacoes[transacoes['tipo'] == 'entrada']['valor'].sum()
total_saidas = transacoes[transacoes['tipo'] == 'saida']['valor'].sum()
saldo = total_entradas - total_saidas

# Agrupamento por Categoria (Essencial para a pergunta de alimentação)
gastos_por_cat = transacoes[transacoes['tipo'] == 'saida'].groupby('categoria')['valor'].sum()

txt_categorias = ""
for categoria, valor in gastos_por_cat.items():
    txt_categorias += f"- {categoria.capitalize()}: R$ {valor:.2f}\n"

txt_produtos = "\n".join([f"- {p['nome']}: {p['rentabilidade']} (Risco: {p['risco']})" for p in produtos])

# ==============================================================================
# 2. MONTAR CONTEXTO (Lógica RAG)
# ==============================================================================
contexto = f"""
=== DADOS DO USUÁRIO ===
Nome: {perfil['nome']}
Perfil: {perfil['perfil_investidor']}
Aceita Risco: {perfil['aceita_risco']}
Objetivo: {perfil['objetivo_principal']}

=== BALANÇO MENSAL ===
Entradas: R$ {total_entradas:.2f}
Saídas: R$ {total_saidas:.2f}
SALDO SOBRANDO: R$ {saldo:.2f}

=== DETALHAMENTO DE GASTOS POR CATEGORIA ===
{txt_categorias}

=== PRODUTOS FINANCEIROS ===
{txt_produtos}
"""

system_prompt = f"""
Você é o Edu, um assistente financeiro. Use estritamente os dados abaixo para responder:
{contexto}

Regras:
1. Se perguntarem sobre uma categoria específica (ex: alimentação), consulte a seção 'DETALHAMENTO DE GASTOS POR CATEGORIA'.
2. Se 'Aceita Risco' for False, não recomende risco ALTO.
"""

# ==============================================================================
# 3. CHAMAR OLLAMA (Via Requests)
# ==============================================================================
def chamar_ollama(mensagens, modelo_nome, url_api):
    payload = {
        "model": modelo_nome,
        "messages": [{'role': 'system', 'content': system_prompt}] + mensagens,
        "stream": False
    }
    try:
        response = requests.post(url_api, json=payload)
        if response.status_code == 200:
            return response.json()['message']['content']
        else:
            return f"Erro Ollama: {response.status_code} - Verifique se baixou o modelo 'ollama pull {modelo_nome}'"
    except:
        return "Erro de Conexão. Verifique se o Ollama está rodando na porta 11434."

# ==============================================================================
# 4. INTERFACE
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Configurações")
    url_config = st.text_input("URL Ollama", value=OLLAMA_URL)
    modelo_config = st.text_input("Modelo", value=MODELO_PADRAO)
    st.divider()
    st.metric("Saldo", f"R$ {saldo:.2f}")
    st.markdown("### Resumo de Gastos")
    st.text(txt_categorias)

st.title("💵 Edu, o Consultor Financeiro")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": f"Oi {perfil['nome']}! Sobraram R$ {saldo:.2f}. Quer saber onde você mais gastou?"})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ex: Quanto gastei com alimentação?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analisando dados..."):
            resp = chamar_ollama(st.session_state.messages, modelo_config, url_config)
            st.markdown(resp)
    
    st.session_state.messages.append({"role": "assistant", "content": resp})
import streamlit as st
import pandas as pd
import json
import os
import ollama  # Biblioteca oficial do Ollama
import requests  

# ==================================CONFIGURAÇÃO DA PÁGINA==================================
st.set_page_config(page_title="Edu | AI Financeiro Local", page_icon="🦙")


OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO_PADRAO = "llama3"

# --- Helper para criar dados mockados se não existirem ---
def setup_dados_iniciais():
    if not os.path.exists("data"):
        os.makedirs("data")
        
    if not os.path.exists("data/perfil_investidor.json"):
        with open("data/perfil_investidor.json", "w", encoding='utf-8') as f:
            json.dump({
                "nome": "Raissa Nunes", 
                "perfil_investidor": "moderado", 
                "aceita_risco": False,
                "objetivo_principal": "Reserva de Emergência"
            }, f)
            
    if not os.path.exists("data/produtos_financeiros.json"):
        with open("data/produtos_financeiros.json", "w", encoding='utf-8') as f:
            json.dump([
                {"nome": "Tesouro Selic", "rentabilidade": "15% a.a.", "risco": "baixo"},
                {"nome": "CDB Banco Seguro", "rentabilidade": "15.2% a.a.", "risco": "baixo"},
                {"nome": "Fundo Ações", "rentabilidade": "Variável", "risco": "alto"}
            ], f)

    if not os.path.exists("data/transacoes.csv"):
        with open("data/transacoes.csv", "w", encoding='utf-8') as f:
            f.write("data,tipo,valor\n2025-10-01,entrada,5000.00\n2025-10-05,saida,2400.00")

setup_dados_iniciais()


# ==================================CARREGA DADOS (Sua estrutura solicitada)==================================
try:
    perfil = json.load(open('data/perfil_investidor.json', encoding='utf-8'))
    produtos = json.load(open('data/produtos_financeiros.json', encoding='utf-8'))
    transacoes = pd.read_csv('data/transacoes.csv')
    historico = pd.read_csv('data/historico_atendimento.csv') 
except FileNotFoundError:
    st.error("Erro: Arquivos de dados não encontrados na pasta /data.")
    st.stop()

# ==================================MONTAR CONTEXTO (RAG Lógico)==================================

total_entradas = transacoes[transacoes['tipo'] == 'entrada']['valor'].sum()
total_saidas = transacoes[transacoes['tipo'] == 'saida']['valor'].sum()
saldo_livre = total_entradas - total_saidas

lista_produtos = "\n".join([f"- {p['nome']} ({p['rentabilidade']} | Risco: {p['risco']})" for p in produtos])

contexto_dados = f"""
=== DADOS DO USUÁRIO ===
Nome: {perfil['nome']}
Perfil: {perfil['perfil_investidor']}
Aceita Risco: {perfil['aceita_risco']} (IMPORTANTE: Se False, não indique risco ALTO)
Objetivo: {perfil['objetivo_principal']}

=== SITUAÇÃO FINANCEIRA ATUAL ===
Entradas: R$ {total_entradas:.2f}
Saídas: R$ {total_saidas:.2f}
SALDO DISPONÍVEL (SOBRAS): R$ {saldo_livre:.2f}

=== PRODUTOS DISPONÍVEIS ===
{lista_produtos}
"""

# ==================================SYSTEM PROMPT==================================
system_prompt = f"""
Você é o Edu, um consultor financeiro pessoal.
Responda sempre com base nos dados fornecidos abaixo. Seja direto e educado.

{contexto_dados}

REGRAS:
1. Se o usuário perguntar quanto sobrou, use o valor exato do SALDO DISPONÍVEL.
2. Se o usuário tiver 'Aceita Risco: False', desencoraje investimentos de risco ALTO.
3. Responda em português do Brasil.
"""

# ==================================CHAMAR OLLAMA (Integração Local)==================================
def chamar_ollama(mensagens_chat, modelo="llama3"):
    """
    Envia o histórico de conversa para o Ollama rodando localmente.
    """
    try:
        # Adiciona o system prompt no início da lista de mensagens para o modelo saber quem ele é
        historico_completo = [{'role': 'system', 'content': system_prompt}] + mensagens_chat
        
        response = ollama.chat(model=modelo, messages=historico_completo)
        return response['message']['content']
    
    except Exception as e:
        return f"Erro ao conectar com Ollama. Verifique se o app está rodando (comando 'ollama serve'). Detalhe: {e}"

# ==================================INTERFACE (Streamlit)==================================

# Sidebar para escolher modelo
with st.sidebar:
    st.header("Configurações LLM")
    modelo_selecionado = st.selectbox("Modelo Ollama", ["llama3", "mistral", "phi3", "gemma:2b"])
    st.info(f"Rodando localmente via Ollama.\n\nCertifique-se de ter baixado o modelo: \n`ollama pull {modelo_selecionado}`")
    
    st.divider()
    st.write(f"**Cliente:** {perfil['nome']}")
    st.metric("Sobras do Mês", f"R$ {saldo_livre:.2f}")

st.title("Edu Financeiro (Local AI)")

# Inicializar sessão de chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem inicial do bot
    st.session_state.messages.append({"role": "assistant", "content": f"Oi {perfil['nome']}! Vi que sobraram R$ {saldo_livre:.2f}. Quer ajuda?"})

# Exibir mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input do usuário
if prompt := st.chat_input("Pergunte sobre suas finanças..."):
    # 1. Mostrar pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Gerar resposta com Ollama
    with st.chat_message("assistant"):
        with st.spinner(f"Pensando com {modelo_selecionado}..."):
            # Envia apenas o histórico (o system prompt é injetado dentro da função chamar_ollama)
            resposta = chamar_ollama(st.session_state.messages, modelo=modelo_selecionado)
            st.markdown(resposta)
    
    # 3. Salvar resposta
    st.session_state.messages.append({"role": "assistant", "content": resposta})
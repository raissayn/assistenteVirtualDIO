import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO PADRÃO ============
DEFAULT_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3:8b" 

st.set_page_config(page_title="Edu | Educador Financeiro", page_icon="🎓", layout="wide")

# ============ CARREGAR DADOS ============
try:
    perfil = json.load(open('./data/perfil_investidor.json', encoding='utf-8'))
    transacoes = pd.read_csv('./data/transacoes.csv')
    historico = pd.read_csv('./data/historico_atendimento.csv')
    produtos = json.load(open('./data/produtos_financeiros.json', encoding='utf-8'))
except FileNotFoundError:
    st.error("Erro: Arquivos de dados não encontrados na pasta ./data")
    st.stop()

# ============ CÁLCULOS PARA O DASHBOARD (SIDEBAR) ============

total_entradas = transacoes[transacoes['tipo'] == 'entrada']['valor'].sum()
total_saidas = transacoes[transacoes['tipo'] == 'saida']['valor'].sum()
saldo_atual = total_entradas - total_saidas


gastos_por_categoria = transacoes[transacoes['tipo'] == 'saida'].groupby('categoria')['valor'].sum()
txt_resumo_gastos = ""
for cat, val in gastos_por_categoria.items():
    txt_resumo_gastos += f"- {cat.capitalize()}: R$ {val:.2f}\n"

# ============ SIDEBAR (CONFIGURAÇÕES & RESUMO) ============
with st.sidebar:
    st.header("⚙️ Configurações")
    

    url_ollama = st.text_input("URL Ollama", value=DEFAULT_URL)
    modelo_ollama = st.text_input("Modelo", value=DEFAULT_MODEL)
    
    st.divider()
    
    # Dashboard LATERAL
    st.subheader("💰 Painel do Cliente")
    st.write(f"**Cliente:** {perfil['nome']}")
    
    st.metric("Saldo Disponível", f"R$ {saldo_atual:.2f}")
    
    st.divider()
    
    st.subheader("📊 Gastos por Categoria")
    st.markdown(txt_resumo_gastos)

# ============ MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

BALANÇO FINANCEIRO ATUAL:
- Total Entradas: R$ {total_entradas:.2f}
- Total Saídas: R$ {total_saidas:.2f}
- Saldo Livre: R$ {saldo_atual:.2f}

RESUMO DE GASTOS POR CATEGORIA:
{txt_resumo_gastos}

TRANSAÇÕES DETALHADAS:
{transacoes.to_string(index=False)}

PRODUTOS DISPONÍVEIS NA CORRETORA:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o Edu, um educador financeiro amigável e didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
- Use os dados do 'BALANÇO FINANCEIRO' e 'RESUMO DE GASTOS' para responder sobre valores.
- NUNCA recomende investimentos específicos (como "compre X"), apenas explique os produtos disponíveis.
- Linguagem simples, como se explicasse para um amigo.
- Se não souber algo, admita.
- Responda de forma sucinta e direta.
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg, url, modelo):
    prompt_completo = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    PERGUNTA DO USUÁRIO: {msg}
    
    RESPOSTA DO EDU:
    """

    try:
        r = requests.post(url, json={"model": modelo, "prompt": prompt_completo, "stream": False})
        if r.status_code == 200:
            return r.json()['response']
        else:
            return f"Erro no Ollama ({r.status_code}): Verifique se o modelo '{modelo}' está baixado."
    except requests.exceptions.ConnectionError:
        return "Erro de conexão: O Ollama parece estar desligado."

# ============ INTERFACE PRINCIPAL ============
st.title("💵 Edu | Educador Financeiro")

if "messages" not in st.session_state:
    st.session_state.messages = []

    # Mensagem de boas-vindas 
    welcome = f"Olá {perfil['nome']}! Vi aqui no painel que sobraram R$ {saldo_atual:.2f}. Como posso ajudar?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input do usuário
if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)
    
    with st.chat_message("assistant"):
        with st.spinner("Consultando dados..."):
            resposta = perguntar(pergunta, url_ollama, modelo_ollama)
            st.markdown(resposta)
    
    st.session_state.messages.append({"role": "assistant", "content": resposta})
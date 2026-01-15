# 💰 Edu – Assistente Financeiro Pessoal (IA Local)

O **Edu** é um assistente virtual focado em **finanças pessoais** que roda **100% localmente** na sua máquina. Ele utiliza a tecnologia **RAG (Retrieval-Augmented Generation)** para ler dados financeiros (extratos CSV e perfis JSON) e fornecer **consultoria personalizada e segura**, respeitando o perfil de risco do usuário.

O projeto utiliza **Streamlit** para a interface web e **Ollama** para executar **Modelos de Linguagem (LLMs)** como **Llama 3** ou **Mistral** localmente, garantindo **privacidade total dos dados**.

---

## 🚀 Funcionalidades

- **Consultoria Personalizada**  
  Analisa o perfil do investidor (Conservador / Moderado / Arrojado) antes de fornecer recomendações.

- **Análise de Fluxo de Caixa**  
  Lê arquivos `.csv` de transações, calcula entradas e saídas e identifica o saldo disponível em tempo real.

- **Suitability (Trava de Segurança)**  
  Se o perfil do usuário não aceita risco, a IA **nunca** recomendará investimentos de alto risco (Ações / Cripto), mesmo que solicitada.

- **Privacidade Total**  
  Nenhum dado financeiro é enviado para a nuvem (OpenAI / Google). Todo o processamento ocorre localmente.

- **Configurável**  
  Permite trocar o modelo de IA (Llama3, Phi3, Mistral) diretamente pela interface.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- Streamlit (Interface Frontend)
- Ollama (Servidor de LLM Local)
- Pandas (Manipulação de Dados)
- Requests (Comunicação com a API do Ollama)

---

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python** (versão 3.10 ou superior)
- **Ollama**
  - Baixe e instale em: https://ollama.com
  - Após instalar, abra o terminal e baixe um modelo (exemplo: Llama 3):

```bash
ollama pull llama3:8b
```
## 📦 Instalação e Execução

Siga os passos abaixo para rodar o projeto.
1. Clone o repositório
```bash

git clone https://github.com/SEU-USUARIO/assistente-financeiro-edu.git
cd assistente-financeiro-edu
```
2. Crie um Ambiente Virtual (Recomendado)

Para evitar conflitos com o Python do sistema, crie um ambiente isolado.

No Linux/Mac:
```bash

python3 -m venv .venv
source .venv/bin/activate
```
No Windows:
Bash
```bash
python -m venv .venv
.venv\Scripts\activate
```
3. Instale as dependências
```bash
pip install streamlit pandas requests
```
4. Certifique-se que o Ollama está rodando

Abra um terminal separado e digite:
```bash
ollama serve
```
(Se você instalou o app desktop do Ollama, ele provavelmente já está rodando em segundo plano).
5. Execute a aplicação
```bash
streamlit run src/app.py
```
O navegador abrirá automaticamente no endereço: http://localhost:8501.

## 🧠 Como Utilizar

    Dashboard Lateral:

        Verifique o Perfil Carregado (Ex: Raissa Nunes).
        Veja o Saldo Calculado do mês (baseado no CSV).
        Em Configurações, você pode alterar o modelo da IA (caso tenha baixado outro, como mistral ou phi3).

    Chat:
        Pergunte sobre sua situação: "Quanto sobrou este mês?"
        Peça recomendações: "Onde posso investir esse valor?"
        Teste a segurança: "Devo colocar minha reserva de emergência em ações?" (O Edu deve negar se seu perfil for conservador, pois as respostas são baseadas no perfil de cada consumidor!).


## 📝 Licença

Este projeto é de código aberto para fins educacionais, criado a partir do desafio final da plataforma DIO (Desafio de Projeto Final — Construa seu Assistente Virtual com IA Generativa). Sinta-se à vontade para modificar e melhorar! 
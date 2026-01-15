### 💰 Edu - Assistente Financeiro Pessoal (IA Local)

O Edu é um assistente virtual focado em finanças pessoais que roda 100% localmente na sua máquina. Ele utiliza a tecnologia RAG (Retrieval-Augmented Generation) para ler dados financeiros (extratos CSV e perfis JSON) e fornecer consultoria personalizada e segura, respeitando o perfil de risco do usuário.

Este projeto utiliza Streamlit para a interface web e Ollama para rodar Modelos de Linguagem (LLMs) como Llama 3 ou Mistral localmente, garantindo privacidade total dos dados.

#### - 🚀 Funcionalidades
    - Consultoria Personalizada: Analisa o perfil do investidor (Conservador/Moderado/Arrojado) antes de dar dicas.

    - Análise de Fluxo de Caixa: Lê arquivos .csv de transações, calcula entradas/saídas e identifica o saldo disponível em tempo real.

    - Suitability (Trava de Segurança): Se o perfil do usuário não aceita risco, a IA é programada para nuncar recomendar investimentos de alto risco (Ações/Cripto), mesmo que perguntada.

    - Privacidade Total: Nenhum dado financeiro é enviado para nuvem (OpenAI/Google). Tudo é processado no seu computador.

    - Configurável: Permite trocar o modelo de IA (Llama3, Phi3, Mistral) diretamente pela interface.

### - 🛠️ Tecnologias Utilizadas

    Python 3.10+

    Streamlit (Interface Frontend)

    Ollama (Servidor de LLM Local)

    Pandas (Manipulação de Dados)

    Requests (Comunicação com API do Ollama)

### - ⚙️ Pré-requisitos

Antes de começar, você precisa ter instalado na sua máquina:

    Python (Versão 3.10 ou superior).

    Ollama:

        Baixe e instale em ollama.com.

        Após instalar, abra o terminal e baixe um modelo (ex: Llama 3):
        Bash

    ollama pull llama3:8b

* Nota: O modelo usado por padrão no código é o llama3:8b. Se baixar outro, lembre-se de alterar na interface.

### 📦 Instalação e Execução

Siga os passos abaixo para rodar o projeto.
1. Clone o repositório
Bash

git clone https://github.com/SEU-USUARIO/assistente-financeiro-edu.git
cd assistente-financeiro-edu

2. Crie um Ambiente Virtual (Recomendado)

Para evitar conflitos com o Python do sistema, crie um ambiente isolado.

No Linux/Mac:
Bash

python3 -m venv .venv
source .venv/bin/activate

No Windows:
Bash

python -m venv .venv
.venv\Scripts\activate

3. Instale as dependências
Bash

pip install streamlit pandas requests

4. Certifique-se que o Ollama está rodando

Abra um terminal separado e digite:
Bash

ollama serve

(Se você instalou o app desktop do Ollama, ele provavelmente já está rodando em segundo plano).
5. Execute a aplicação
Bash

streamlit run src/app.py

O navegador abrirá automaticamente no endereço: http://localhost:8501.

### 🧠 Como Utilizar

    Dashboard Lateral:

        Verifique o Perfil Carregado (Ex: Raissa Nunes).
        Veja o Saldo Calculado do mês (baseado no CSV).
        Em Configurações, você pode alterar o modelo da IA (caso tenha baixado outro, como mistral ou phi3).

    Chat:
        Pergunte sobre sua situação: "Quanto sobrou este mês?"
        Peça recomendações: "Onde posso investir esse valor?"
        Teste a segurança: "Devo colocar minha reserva de emergência em ações?" (O Edu deve negar se seu perfil for conservador, pois as respostas são baseadas no perfil de cada consumidor!).


### 📝 Licença

Este projeto é de código aberto para fins educacionais, criado a partir do desafio final da plataforma DIO (Desafio de Projeto Final — Construa seu Assistente Virtual com IA Generativa). Sinta-se à vontade para modificar e melhorar! 
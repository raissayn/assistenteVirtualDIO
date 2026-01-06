# Base de Conhecimento

## Dados Utilizados

Para garantir que o **Edu** forneça respostas precisas e não alucine, combinamos dados proprietários (simulados para o desafio) com datasets robustos de mercado obtidos no Hugging Face, adaptados para o contexto brasileiro.

| Arquivo/Dataset | Formato | Origem | Utilização no Agente |
|-----------------|---------|--------|----------------------|
| `produtos_investimento.csv` | CSV | Interno (Mock) | Catálogo de produtos (CDBs, LCIs, Fundos) com taxas, liquidez e risco. |
| `perfil_cliente_mock.json` | JSON | Interno (Mock) | Dados fictícios de clientes para testar personalização (sem dados reais). |
| `financial_phrasebank` | Dataset | Hugging Face | Base para análise de sentimento de mercado e terminologia financeira contextual. |
| `glossario_financeiro_ptbr.json` | JSON | Curadoria Própria | Definições simples para termos complexos (ex: "Benchmarking", "Volatilidade"). |
| `historico_duvidas_frequentes.csv` | CSV | Interno | Pares de Pergunta-Resposta para *Few-Shot Learning* no prompt. |

---

## Adaptações nos Dados

Para que o Edu mantenha seu tom de voz "Smart Casual" e respeite as regras de segurança, os dados passaram por um pré-processamento:

1.  **Tradução e Tropicalização:** Datasets do Hugging Face (originalmente em inglês) foram traduzidos e adaptados para a realidade da B3 (ex: troca de *401k* por *Previdência Privada*).
2.  **Simplificação de Colunas:** No arquivo `produtos_investimento.csv`, colunas técnicas complexas foram concatenadas em descrições textuais amigáveis (ex: transformamos `vol_12m: 0.15` em `texto_risco: "O fundo variou bastante no último ano"`).
3.  **Sanitização (Privacidade):** O arquivo `perfil_cliente_mock.json` foi estritamente revisado para garantir que não contenha PII (Personally Identifiable Information) reais, usando apenas personas genéricas (ex: "Maria, perfil Conservador").

---

## Estratégia de Integração

### Como os dados são carregados?
O agente utiliza uma arquitetura **RAG (Retrieval-Augmented Generation)**.
1.  Os arquivos CSV e JSON são convertidos em vetores (embeddings) e armazenados em um **Vector Database** (como FAISS ou ChromaDB) na inicialização do sistema.
2.  Quando o usuário faz uma pergunta, o sistema realiza uma *busca semântica* na base vetorial para encontrar apenas os trechos relevantes (ex: a lâmina específica do fundo perguntado).

### Como os dados são usados no prompt?
Os dados não são "treinados" no modelo, mas sim **injetados dinamicamente** no contexto da mensagem antes de chegar à LLM.
1.  **Input:** Usuário pergunta "O Fundo XPTO é arriscado?"
2.  **Busca:** O sistema recupera a linha do CSV correspondente ao "Fundo XPTO".
3.  **Prompt Engineering:** O dado cru é inserido em um bloco de contexto com instruções de "Grounding" (ancoragem), obrigando o Edu a usar apenas aquele dado para responder.

---

## Exemplos de Contexto Montado

Abaixo está a estrutura exata do prompt que chega ao modelo (LLM) após a recuperação dos dados:

```text
=== INSTRUÇÃO DO SISTEMA ===
Você é o Edu, um consultor financeiro casual e ético.
Responda à pergunta do usuário APENAS com base nos [DADOS RECUPERADOS] abaixo.
Se a resposta não estiver nos dados, diga "Não tenho essa informação".
Não invente números. Lembre-se: você não acessa conta bancária real.

=== DADOS DO CLIENTE (MOCK) ===
- Nome: Carlos "Investidor Iniciante"
- Perfil: Conservador
- Objetivo: Reserva de Emergência

=== DADOS RECUPERADOS (Base de Conhecimento) ===
Produto: Fundo Renda Fixa Super Simples
Risco: Baixo
Liquidez: D+0 (Resgate imediato)
Taxa de Administração: 0.2% a.a.
Rentabilidade 12m: 11.5%
Descrição Técnica: Fundo referenciado DI com baixo risco de crédito.

=== PERGUNTA DO USUÁRIO ===
"Edu, esse fundo 'Super Simples' serve pra eu guardar o dinheiro que posso precisar amanhã? É perigoso?"

=== SUA RESPOSTA ===
(O agente deve gerar a resposta aqui baseada na Liquidez D+0 e Risco Baixo)

----
=== SYSTEM PROMPT (EDU) ===
Você é o Edu, consultor financeiro casual. Use os dados abaixo para responder.
NÃO recomende produtos de risco ALTO se o cliente tiver 'aceita_risco: false'.

=== PERFIL DO CLIENTE ===
Nome: Raissa Nunes (20 anos)
Objetivo Atual: Completar Reserva (Faltam R$ 5.000 para a meta).
Restrição: NÃO aceita risco.
Saldo Disponível Estimado (mês): R$ 2.500 (Baseado nas transações de Out/2025).

=== PRODUTOS DISPONÍVEIS ===
1. Tesouro Selic (Risco Baixo)
2. CDB Liquidez Diária (Risco Baixo, 102% CDI)
3. LCI/LCA (Risco Baixo, Isento IR, trava 90 dias)
4. Fundo Multimercado (Risco Médio)
5. Fundo Ações (Risco Alto)

=== HISTÓRICO ===
Raissa já perguntou sobre CDB e Tesouro anteriormente. Já sabe o básico.

=== PERGUNTA DA RAISSA ===
"Edu, sobrou um dinheiro esse mês. Pensei em colocar naquele Fundo de Ações pra ver se consigo comprar meu apê mais rápido. O que acha?"

=== RESPOSTA ESPERADA DO AGENTE ===
"Oi, Raissa! Que ótimo que sobrou dinheiro! 🎉
Olhando seu perfil aqui, vi que sua prioridade agora é terminar a reserva de emergência (faltam 5k) e que você prefere evitar riscos no momento.
O Fundo de Ações tem risco alto e oscila bastante. Como seu objetivo do apê é pra 2027, que tal focarmos em algo seguro agora?
O 'LCI/LCA' rende bem (95% do CDI) e é isento de imposto, ou o 'CDB Liquidez Diária' se quiser mexer logo. O que acha de garantir a segurança primeiro?"
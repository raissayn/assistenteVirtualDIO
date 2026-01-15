# Avaliação e Métricas (info modelo DIO)

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Cenários Testados no agende EDU


### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** Valor baseado no `transacoes.csv`
- **Resposta resultado:** Raissa Nunes, você gastou R$ 530,00 com alimentação no mês passado.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Produto compatível com o perfil do cliente
- **Resposta resultado:** Como você não aceita risco e seu objetivo é construir reserva de emergência, eu recomendaria o Tesouro Selic ou o CDB Banco Seguro. Esses produtos financeiros oferecem juros baixos e são considerados seguros. Eles podem ajudar a aumentar seu patrimônio líquido sem correr riscos excessivos.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resposta resultado:** Peço desculpas, Raissa Nunes! Eu sou um assistente financeiro e não tenho conhecimento sobre a previsão do tempo. Meu papel é ajudar você com questões financeiras e não meteorológicas.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resposta resultado:** Peço desculpas, Raissa Nunes! Como eu sou um assistente financeiro e tenho informações específicas sobre produtos financeiros, eu posso dizer que não há nenhum produto chamado "XYZ" nos meus dados. Eu só tenho conhecimento sobre Tesouro Selic, CDB Banco Seguro e Fundo Ações Ibov.
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Resultados

Após os testes, conclusões:

**O que funcionou bem, e o que pode melhorar:**
- O agente cumpre o pedido, porém para uma melhor performace deveria responder perguntas sobre investimentos de forma mais completa, e menos resumida.
- Aumentar o conhecimentos dele sobre diferentes tipos de investimentos...

---

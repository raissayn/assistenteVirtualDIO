# Avaliação e Métricas (info modelo DIO)
------------------------------------------
## Como Avaliar o Agente?

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

------------------------------------------

## Cenários Testados no agende EDU


### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** Valor baseado no `transacoes.csv`
- **Resposta resultado:** Raissa! De acordo com o Resumo de Gastos por Categoria, você gastou R$ 530,00 com alimentação.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Produto compatível com o perfil do cliente
- **Resposta resultado:** Raissa, obrigado por confiar em mim!

Antes de qualquer recomendação, é importante entender que o objetivo é construir uma reserva de emergência. Isso significa que precisamos priorizar produtos com baixo risco e rentabilidade estável.

Considerando seu patrimônio de R 15.000,00 e sua reserva atual de R 10.000,00, você tem uma boa base para começar a construir essa reserva.

Entre os produtos disponíveis, eu diria que o Tesouro Selic e o CDB Banco Seguro são opções interessantes. Ambos oferecem uma rentabilidade estável de cerca de 15% ao ano e um risco baixo.

O Tesouro Selic é um investimento governo que garante a segurança dos seus depósitos, enquanto o CDB Banco Seguro é um certificado de depósito bancário com uma rentabilidade fixa.

Eu não recomendaria o Fundo Ações Ibov porque, embora possa oferecer uma rentabilidade mais alta, também apresenta um risco maior. Como você está construindo uma reserva de emergência, priorizo produtos com baixo risco e rentabilidade estável.

Qual é sua opinião sobre essas opções?
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resposta resultado:** Amiga Raissa, como eu não tenho nada a ver com o tempo climático, não posso fazer uma previsão para você! Eu sou um educador financeiro, então vou me concentrar em sua situação financeira. Vamos trabalhar juntos para construir essa reserva de emergência que você deseja!

Vou analisar seus dados e encontrar formas eficazes para alcançar seu objetivo. Qualquer dúvida ou preocupação que você tenha sobre suas finanças, estou aqui para ajudá-la!
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resposta resultado:** Eu não posso fornecer informações sobre um produto chamado "XYZ" porque isso é específico e eu não tenho essa informação. Além disso, como educador financeiro, minha responsabilidade é explicar conceitos de finanças pessoais, usando os dados do cliente como exemplos práticos.

Vamos focar em construir reserva de emergência para a Raissa Nunes. Com o objetivo de ajudá-la a alcançar esse objetivo, gostaria de perguntar: você gostaria de saber mais sobre os produtos disponíveis na corretora e como eles podem ser usados para construir sua reserva?
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Resultados

Após os testes, conclusões:

**O que funcionou bem, e o que pode melhorar:**
- O agente cumpre o objetivo, porém para uma melhor performace, deveriamos realizar um melhor aprimoramento, aumentando o conhecimentos dele sobre diferentes tipos de investimentos...
- Aumentar a base de produtos financeiros (produtos_financeiros.json)

---

... pretendo testar novos testes/usuários para refinar os prompts ... 

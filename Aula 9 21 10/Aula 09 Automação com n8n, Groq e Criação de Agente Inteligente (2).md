# 🤖 Aula 09 — Automação com n8n, Groq e Criação de Agente Inteligente

**Disciplina:** Tópicos Especiais em Programação  
**Data:** 21/10/2025  
Eduardo Possamai  

---

## 🧠 Objetivo da Aula

A aula teve como foco aprofundar o uso do **n8n** para automação de processos e integração entre APIs, explorando a criação de **fluxos manuais e automáticos**, além da utilização do **Groq** para geração de respostas dinâmicas.  

O ponto central foi a construção de um **agente inteligente**, capaz de **interpretar mensagens recebidas, aplicar lógica personalizada e responder conforme uma persona definida**.

---

## 🧩 Conceitos Trabalhados

- **Fluxos no n8n**: execução manual e automática (via gatilhos e endpoints).  
- **Integração com API do Groq** para geração de texto e respostas dinâmicas.  
- **Criação de agentes personalizados** no n8n.  
- **Manipulação de JSON** para interpretar e estruturar mensagens recebidas.  
- **Configuração de respostas automatizadas** com base em contexto e persona.

---

## ⚙️ Desenvolvimento da Aula

### 🔹 1. Criação dos Fluxos no n8n
Foram criados dois tipos principais de fluxo:

- **Fluxo manual** – executado diretamente na interface do n8n para testes.  
- **Fluxo automático** – configurado para disparar a partir de eventos (mensagens ou requisições HTTP).  

Cada fluxo foi composto por nós como:
- **Webhook / Trigger**: ponto de entrada das mensagens;  
- **Function / Code Node**: manipulação e tratamento de dados JSON;  
- **HTTP Request**: integração com a API do Groq para gerar respostas;  
- **Respond to Webhook**: envio da resposta final.

---

### 🔹 2. Integração com o Groq
Utilizou-se o Groq para gerar textos dinâmicos de resposta.  
A configuração incluiu a chave de API e o uso do modelo de linguagem selecionado.  
Exemplo simplificado do corpo da requisição no n8n (HTTP Node):

```json
{
  "model": "groq-large",
  "input": "Responda de forma simpática a mensagem recebida: {{$json['mensagem']}}"
}
O retorno da API foi tratado e repassado ao nó seguinte, que formatava a mensagem antes de enviá-la ao destinatário via API do Evolution.
### 🔹 3. Criação do Agente Inteligente

O agente foi projetado para **responder mensagens automaticamente com base em uma persona definida**, combinando:

- **Entrada:** mensagem JSON recebida via webhook;
    
- **Processamento:** Groq + lógica condicional;
    
- **Saída:** resposta formatada enviada via Evolution.
    

A persona foi definida dentro do fluxo, controlando o **tom de voz e comportamento do agente** (ex: assistente amigável, profissional, informal, etc.).

Exemplo de estrutura JSON utilizada:
{
  "mensagem": "Olá, tudo bem?",
  "remetente": "Usuário",
  "persona": "Assistente simpático que responde de forma leve e cordial."
}
O agente interpretava esse conteúdo, repassava o texto ao Groq e devolvia a resposta já personalizada conforme a persona.

### 🔹 4. Manipulação de JSON e Formatação de Mensagens

Durante o desenvolvimento, foi necessário:

- Extrair campos específicos de objetos JSON (`mensagem`, `remetente`, `hora`, etc.);
    
- Formatar respostas em novos objetos;
    
- Validar campos vazios ou incorretos antes de chamar a API;
    
- Gerar logs de resposta dentro do n8n para depuração.
    

Exemplo de saída formatada:
{
  "resposta": "Oi! Que bom te ouvir 😊 Como posso te ajudar hoje?",
  "status": "enviada"
}

# ⚙️ Aula 08 — Gerenciamento de Serviços no Portainer (Postgres, Redis, EvolutionV2 e n8n)

**Disciplina:** Tópicos Especiais em Programação  
**Data:** 14/10/2025  
Eduardo Possamai

---

## 🧠 Objetivo da Aula

Nesta aula, continuamos a configuração do nosso ambiente na Oracle Cloud. Você aprenderá a usar o Portainer como interface principal para gerenciar containers Docker e verá o passo a passo da implantação dos serviços Postgres, Redis, EvolutionV2 e n8n. Para validar a instalação, faremos um teste prático de integração entre o n8n e a API do Evolution, simulando o envio de mensagens automatizadas.
---

## 🌐 Contexto

Com o Portainer já em execução (implantado na Aula 07), a aula focou em:
- Criar novas *stacks* diretamente pela interface do Portainer;  
- Implantar serviços interligados via Docker Network;  
- Modificar variáveis e parâmetros nos arquivos `docker-compose` (YAML);  
- Testar fluxos reais entre containers.

O objetivo foi compreender a **comunicação e integração entre diferentes serviços** dentro do mesmo ambiente.

---

## 🧩 Serviços Implantados

| ID | Serviço | Função |
|----|----------|--------|
| 3 | **Redis** | Armazenamento em memória e filas para o Evolution |
| 4 | **Postgres** | Banco de dados para persistência dos serviços |
| 5 | **n8n** | Orquestrador de automações e fluxos visuais |
| 6 | **EvolutionV2** | API de mensageria e integração com o n8n |

---

## ⚙️ Configurações Realizadas

### 🔹 Postgres
Banco de dados de apoio aos serviços:
```yaml
version: "3.8"
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: <usuario>
      POSTGRES_PASSWORD: <senha>
      POSTGRES_DB: evolution
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
volumes:
  postgres_data:
🔹 Redis
Sistema de cache e mensageria:
version: "3.8"
services:
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
- Implantado e validado via logs.
    
- Comunicação funcional com o **EvolutionV2**.
  
🔹 EvolutionV2
Serviço de automação e mensageria integrado a Redis e Postgres:
version: "3.8"
services:
  evolutionv2:
    image: atendai/evolution-api-v2:latest
    ports:
      - "8081:8081"
    environment:
      DATABASE_URL: postgres://<usuario>:<senha>@postgres:5432/evolution
      REDIS_HOST: redis
      REDIS_PORT: 6379
      NODE_ENV: production
    depends_on:
      - postgres
      - redis
- Implantado e testado via API local (`porta 8081`).
  
- Comunicação validada entre containers.
🔹 n8n (Orquestrador de Fluxos)
version: "3.8"
services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=<usuario>
      - N8N_BASIC_AUTH_PASSWORD=<senha>
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:
- Implantado como último serviço.
    
- Acesso via navegador:
http://<IP_DA_INSTÂNCIA>:5678
Criado um **fluxo de teste** no n8n:

- **Trigger:** Manual
    
- **Ação:** Envio de mensagem via endpoint da **API do Evolution**
    
- **Resultado:** Fluxo concluído com sucesso, mensagem transmitida corretamente.

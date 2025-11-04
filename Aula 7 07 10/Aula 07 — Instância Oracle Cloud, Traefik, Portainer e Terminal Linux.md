# ☁️ Aula 07 — Instância Oracle Cloud, Traefik, Portainer e Terminal Linux

**Disciplina:** Tópicos Especiais em Programação  
**Data:** 07/10/2025  
Eduardo Possamai 

---

## Resumo
sta aula detalha o provisionamento de uma instância Oracle Cloud (Always Free), desde a criação até a validação do acesso remoto via PowerShell/SSH. O foco principal é a configuração do ambiente de containers Docker, com a instalação dos serviços essenciais Traefik (reverse proxy) e Portainer (admin UI). A prática também abrange comandos Linux fundamentais para a manutenção do sistema.

---

## Ambiente e Premissas
- **SO da VM:** Oracle Linux 8  
- **Shape:** VM.Standard.E2.1.Micro (eligible Always Free)  
- **Acesso:** usuário `opc` via **SSH** (chave `.pem`)  
- **Container Runtime:** Docker  
- **Serviços:** `traefik_traefik` (Traefik) e `portainer` (Portainer)

---

## O que foi feito (visão técnica)
A instância foi criada no OCI e acessada via **PowerShell** para validação de rede e sistema. Com o Docker ativo, foram definidos dois serviços:  
- **Traefik**, exposto para tráfego Web e com dashboard;  
- **Portainer**, persistente, responsável pelo gerenciamento visual dos containers/stacks.

A configuração priorizou **stack YAML** (em vez de `docker run`) para manter o ambiente declarativo e versionável. Após o deploy, foi verificada a disponibilidade via navegador (Portainer em `:9000`) e o tempo de estabilização operacional (≈1–5 min).

---

## Configurações aplicadas (essência)
- **Serviço Traefik**
  - Nome do serviço: `traefik_traefik`  
  - Função: reverse proxy e painel de observabilidade  
  - Orquestração por stack (`traefik.yaml`)

- **Serviço Portainer**
  - Função: gerenciamento de containers/stacks via Web UI  
  - Persistência em volume (`/data`)  
  - Acesso: `http://<IP_DA_INSTÂNCIA>:9000/`  
  - Inicialização típica: ~1 min (até 5 min para estabilizar)

---

## Comandos utilizados (referência rápida)
> SSH, diagnóstico e sistema
```bash
ssh -i caminho_da_chave.pem opc@<IP>   # acesso remoto
ping <IP>                              # teste de rede
uname -a                               # kernel/SO
uptime                                 # carga e tempo ligado

Docker (instalação/serviço)
sudo apt update -y && sudo apt upgrade -y
sudo apt install docker.io -y
sudo systemctl enable docker && sudo systemctl start docker
docker ps

Edição/arquivos (YAML e texto)
nano traefik.yaml        # editor simples
vim traefik.yaml         # editor avançado (i, esc, :wq / :x / :!)
touch nome_arquivo       # criar arquivo

Deploy e gerenciamento das stacks
sudo docker stack deploy --prune --resolve-image always -c traefik.yaml traefik
sudo docker stack deploy -c portainer.yaml portainer

Conceitos de permissões e utilitários
r = read  | w = write | x = execute
chmod      # alterar permissões
ls, ls -l, ls -la, cd, mkdir, rm, cat
sudo       # elevação de privilégio
&&         # encadear comandos

## Referências

- Oracle Cloud Free Tier — [https://www.oracle.com/cloud/free/](https://www.oracle.com/cloud/free/)
    
- Traefik Docs — https://doc.traefik.io/traefik/
    
- Portainer Docs — https://docs.portainer.io/
    
- Guia CLI Linux (Ubuntu) — [https://ubuntu.com/tutorials/command-line-for-beginners](https://ubuntu.com/tutorials/command-line-for-beginners)
import streamlit as st
import requests
import base64
import uuid
from datetime import datetime
import io

# --- CONFIGURAÇÃO DA PÁGINA E ESTADO INICIAL ---

st.set_page_config(layout="wide", page_title="Cloudflare AI Image Generator")

# Inicializa o estado da sessão para o histórico e outros controles
if 'history' not in st.session_state:
    st.session_state.history = []
if 'main_image' not in st.session_state:
    st.session_state.main_image = None
if 'page' not in st.session_state:
    st.session_state.page = 0

# --- FUNÇÕES AUXILIARES ---

def generate_image(prompt, width, height, steps, guidance):
    """Dispara a chamada HTTP para o endpoint do proxy e retorna a resposta."""
    endpoint = "https://ai-image-proxy.joao-theodoro.workers.dev"
    headers = {"Content-Type": "application/json"}
    body = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_inference_steps": steps,
        "guidance_scale": guidance
    }
    try:
        response = requests.post(endpoint, headers=headers, json=body, timeout=180) # Timeout de 3 min
        response.raise_for_status() # Lança erro para status HTTP 4xx/5xx
        return response
    except requests.exceptions.RequestException as e:
        return e

def get_data_url(image_bytes):
    """Converte bytes de imagem em uma data URL."""
    b64_str = base64.b64encode(image_bytes).decode()
    return f"data:image/png;base64,{b64_str}"

# --- INTERFACE DO USUÁRIO (UI) ---

st.title("🚀 Cloudflare AI Image Generator")

# Colunas para o layout principal
col1, col2 = st.columns([0.6, 0.4])

with st.sidebar:
    st.header("🎨 Parâmetros de Geração")
    
    prompt = st.text_area("1. Descreva a imagem (estilo, cena, qualidade…)", height=150,
        placeholder="um pôr do sol futurista em neon, cidade cyberpunk com arranha-céus iluminados, foto realista")
    
    st.write("2. Inputs Numéricos (Opcionais)")
    width = st.number_input("Width", min_value=256, max_value=2048, value=1024, step=64)
    height = st.number_input("Height", min_value=256, max_value=2048, value=1024, step=64)
    steps = st.number_input("num_inference_steps (Steps)", min_value=1, max_value=100, value=30, step=1)
    guidance = st.number_input("guidance_scale (Guidance)", min_value=0.0, max_value=20.0, value=3.5, step=0.1)

    if st.button("Gerar Imagem", use_container_width=True, type="primary"):
        if prompt:
            with st.spinner("Gerando imagem... Isso pode levar alguns segundos."):
                response = generate_image(prompt, width, height, steps, guidance)

                if isinstance(response, requests.Response):
                    try:
                        result_json = response.json()
                        if "result" in result_json and "image" in result_json["result"]:
                            image_b64 = result_json["result"]["image"]
                            data_url = f"data:image/png;base64,{image_b64}"
                            
                            # Guarda a imagem principal para exibição
                            st.session_state.main_image = {
                                "id": str(uuid.uuid4()),
                                "createdAt": datetime.now().isoformat(),
                                "prompt": prompt,
                                "params": {"width": width, "height": height, "steps": steps, "guidance": guidance},
                                "dataUrl": data_url
                            }
                            # Adiciona ao início do histórico
                            st.session_state.history.insert(0, st.session_state.main_image)
                        else:
                            st.error(f"Erro na resposta da API: JSON não contém 'result.image'. Resposta: {result_json}")
                    except Exception as e:
                        st.error(f"Erro ao processar a resposta JSON: {e}")

                else: # Tratamento de erro de conexão
                    st.error(f"Erro de Conexão: {response}")
        else:
            st.warning("Por favor, insira um prompt para gerar a imagem.")


# --- VISOR PRINCIPAL DA IMAGEM ---
with col1:
    st.subheader("Visor Principal")
    if st.session_state.main_image:
        img_item = st.session_state.main_image
        # <<< CORREÇÃO AQUI
        st.image(img_item["dataUrl"], caption=f"Prompt: {img_item['prompt']}", use_container_width=True)
        
        # Converte data URL para bytes para o botão de download
        img_bytes = base64.b64decode(img_item["dataUrl"].split(",")[1])
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.download_button("Baixar PNG", data=img_bytes, file_name=f"{img_item['prompt'][:30].replace(' ', '_')}.png", mime="image/png", use_container_width=True)
        with btn_col2:
            if st.button("Limpar", use_container_width=True):
                st.session_state.main_image = None
                st.rerun()

    else:
        st.info("A imagem gerada aparecerá aqui.")


# --- PAINEL DE HISTÓRICO ---
with col2:
    st.subheader(f"Histórico ({len(st.session_state.history)} imagens)")

    if st.session_state.history:
        # Controles do Histórico
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([0.5, 0.3, 0.2])
        with ctrl_col1:
            filter_text = st.text_input("Filtrar por prompt", label_visibility="collapsed", placeholder="Filtrar por prompt...").lower()
        with ctrl_col2:
            sort_order = st.selectbox("Ordenar", ["Mais recentes", "Mais antigas"], label_visibility="collapsed")
        with ctrl_col3:
            if st.button("Limpar tudo", use_container_width=True):
                st.session_state.history = []
                st.session_state.main_image = None
                st.rerun()
        
        # Aplica filtros e ordenação
        filtered_history = [item for item in st.session_state.history if filter_text in item['prompt'].lower()]
        sorted_history = sorted(filtered_history, key=lambda x: x['createdAt'], reverse=(sort_order == 'Mais recentes'))

        # Paginação
        items_per_page = 10
        start_index = st.session_state.page * items_per_page
        end_index = start_index + items_per_page
        paginated_history = sorted_history[start_index:end_index]
        
        page_col1, page_col2 = st.columns(2)
        with page_col1:
            if start_index > 0:
                if st.button("◀️ Anterior", use_container_width=True):
                    st.session_state.page -= 1
                    st.rerun()
        with page_col2:
            if end_index < len(sorted_history):
                if st.button("Próxima ▶️", use_container_width=True):
                    st.session_state.page += 1
                    st.rerun()

        # Grade de Miniaturas
        st.markdown("---")
        for item in paginated_history:
            st.image(item['dataUrl'], width=180, caption=f"{item['prompt'][:40]}...")
            
            p = item['params']
            st.caption(f"Params: {p['width']}x{p['height']}, {p['steps']} steps")

            card_cols = st.columns(3)
            with card_cols[0]:
                if st.button("Reabrir", key=f"reopen_{item['id']}", use_container_width=True):
                    st.session_state.main_image = item
                    st.rerun()
            with card_cols[1]:
                img_bytes_hist = base64.b64decode(item["dataUrl"].split(",")[1])
                st.download_button("Baixar", data=img_bytes_hist, file_name=f"{item['prompt'][:30]}.png", mime="image/png", key=f"download_{item['id']}", use_container_width=True)
            with card_cols[2]:
                if st.button("Remover", key=f"remove_{item['id']}", use_container_width=True):
                    st.session_state.history = [h for h in st.session_state.history if h['id'] != item['id']]
                    st.rerun()
            st.markdown("---")
            
    else:
        st.info("O seu histórico de imagens aparecerá aqui.")
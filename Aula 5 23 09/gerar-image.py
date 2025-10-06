import requests
import os

# --- SUAS CREDENCIAIS AQUI ---
# Substituímos os valores pelos que você forneceu.
ACCOUNT_ID = "d924dcfb64f8d86e3253325dc0cf7253"
API_TOKEN = "G3qWwft1sf83J1VEoi-5yaiTVuc9tjq5pVQ3UJpO"

# --- CONFIGURAÇÃO DA REQUISIÇÃO ---
# O modelo de IA para geração de imagem.
MODELO = "@cf/stabilityai/stable-diffusion-xl-base-1.0" # Usando um modelo popular, você pode trocar se preferir.
# URL completa da API, construída com seu Account ID.
API_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODELO}"

# Cabeçalhos da requisição com seu token de autorização.
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
}

# --- DADOS PARA A GERAÇÃO DA IMAGEM ---
# Você pode alterar o "prompt" para criar qualquer imagem que desejar.
DATA = {
    "prompt": "A futuristic superbike at sunset, with neon lights reflecting on the horizon.",
}

print("Gerando a imagem, por favor aguarde...")

# --- EXECUÇÃO ---
try:
    # Faz a requisição POST para a API da Cloudflare
    response = requests.post(API_URL, headers=HEADERS, json=DATA)

    # Verifica se a requisição foi bem-sucedida (código 200)
    if response.status_code == 200:
        # A API retorna os dados da imagem diretamente.
        # Salvamos esses dados em um arquivo .png
        with open("imagem_gerada.png", "wb") as img_file:
            img_file.write(response.content)
        print("\nSucesso! Imagem salva como 'imagem_gerada.png'")
        print(f"Abra o arquivo '{os.path.abspath('imagem_gerada.png')}' para ver o resultado.")
    else:
        # Se houver um erro, exibe o código e a mensagem de erro.
        print(f"\nErro ao gerar a imagem.")
        print(f"Status Code: {response.status_code}")
        print(f"Resposta da API: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"\nOcorreu um erro de conexão: {e}")
except Exception as e:
    print(f"\nOcorreu um erro inesperado: {e}")

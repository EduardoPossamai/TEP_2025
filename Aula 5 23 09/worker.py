import requests

# URL base da API Cloudflare
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/d924dcfb64f8d86e3253325dc0cf7253/ai/run/"

# Token correto (sem { } e sem - no final)
headers = {
    "Authorization": "Bearer G3qWwft1sf83J1VEoi-5yaiTVuc9tjq5pVQ3UJpO"
}

def run(model, inputs):
    input_data = {"messages": inputs}
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input_data)
    return response.json()

# Prompt de exemplo
inputs = [
    {"role": "system", "content": "You are a friendly assistant that helps write stories"},
    {"role": "user", "content": "Write a short story about a llama that goes on a journey to find an orange cloud"}
]

# Executa o modelo
output = run("@cf/meta/llama-3-8b-instruct", inputs)

# Imprime a resposta
print(output)

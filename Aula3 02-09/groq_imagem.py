import os
from dotenv import load_dotenv
from groq import Groq

# Carrega o .env automaticamente
load_dotenv()

# Inicializa o cliente com a chave da variável de ambiente
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Faz a chamada para o modelo multimodal
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "O que está nessa imagem?"},
                {"type": "image_url",
                 "image_url": {"url": "https://dicas.boisaude.com.br/wp-content/uploads/2020/05/boi-PO.jpg"}}
            ]
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(completion.choices[0].message)
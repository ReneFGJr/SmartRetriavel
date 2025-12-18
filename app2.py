import json
import chromadb
import ollama

# === 1. Carregar vocabulário JSON ===
with open("data/vc.json", "r", encoding="utf-8") as f:
    vocabulario = json.load(f)

# === 2. Criar cliente Chroma (persistente) ===
client = chromadb.PersistentClient(path="db_vocabulario")
collection = client.get_or_create_collection("vocabulario")
# === 4. Função para responder ===
def responder(pergunta, modelo="llama3.2"):
    resultados = collection.query(query_texts=[pergunta], n_results=3)
    contextos = "\n\n".join(resultados["documents"][0])

    prompt = f"""
Você é um especialista em acessibilidade e organização do conhecimento.
Use o vocabulário abaixo para responder à pergunta do usuário.
Extraia as palavras-chave do PERGUNTA.
Utilize somente os termos do vocabulário fornecido.
Responda somente os termos no formato JSON, sem comentários.
Mostre somente as sem as chaves do JSON.

VOCABULÁRIO:
{contextos}

PERGUNTA: {pergunta}

RESPOSTA:
"""

    resposta = ollama.chat(
        model=modelo,
        options={"temperature": 0.1},  # 👈 Aqui está o ajuste
        messages=[{
            "role": "user",
            "content": prompt
        }])

    conteudo = resposta["message"]["content"]
    print("\n🧩 Pergunta:", pergunta)
    print("💬 Resposta:", conteudo)
    return conteudo


# === 5. Teste ===
responder("Quais as tecnologias na organizacao do conhecimento ?")
responder("Qual o uso d AI nas Bibliotecas Escolares ?")
responder("Como a biblioteca escolar pode melhorar para um cego ?")


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
You are an expert in Artificial Intelligence.
Extract the keywords from the QUESTION.
Use only the terms from the provided vocabulary.
Show only with the terms in JSON format, without comments.
Show only the words from the JSON vocabulary.
Do not create, adapt, or infer terms outside of this vocabulary.
Answer in English.

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
responder("Cite um chatbot semelhante ao BARD")
responder("O que é Big Data?")
responder("What is Big Data?")
responder("Cite um método avançado de IA")
responder("Defina Detecção de Linguagem abusiva")
responder("Quais são os sistemas de IA?")


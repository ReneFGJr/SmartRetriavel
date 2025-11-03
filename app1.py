import json
import chromadb
import ollama

# === 1. Carregar vocabulário JSON ===
with open("data/vc.json", "r", encoding="utf-8") as f:
    vocabulario = json.load(f)

# === 2. Criar cliente Chroma (persistente) ===
client = chromadb.PersistentClient(path="db_vocabulario")
collection = client.get_or_create_collection("vocabulario")

# === 3. Inserir apenas se ainda não estiver na base ===
existing = collection.count()
if existing == 0:
    for i, item in enumerate(vocabulario):
        texto = f"{item['termo']}: {item['definicao']}"
        collection.add(ids=[str(i)],
                       documents=[texto],
                       metadatas=[{
                           "termo": item["termo"]
                       }])
    print(f"✅ {len(vocabulario)} termos adicionados ao banco vetorial.")
else:
    print(
        f"📚 Base vetorial já contém {existing} registros — reutilizando aprendizado."
    )


# === 4. Função para responder ===
def responder(pergunta, modelo="llama3.2"):
    resultados = collection.query(query_texts=[pergunta], n_results=3)
    contextos = "\n\n".join(resultados["documents"][0])

    prompt = f"""
Você é um especialista em acessibilidade e organização do conhecimento.
Use o vocabulário abaixo para responder à pergunta do usuário.

VOCABULÁRIO:
{contextos}

PERGUNTA: {pergunta}

RESPOSTA:
"""

    resposta = ollama.chat(model=modelo,
                           messages=[{
                               "role": "user",
                               "content": prompt
                           }])

    conteudo = resposta["message"]["content"]
    print("\n🧩 Pergunta:", pergunta)
    print("💬 Resposta:", conteudo)
    return conteudo


# === 5. Teste ===
responder("O que é BENANCIB?")

import json
import chromadb
import ollama

# === 1. Carregar vocabulário JSON ===
with open("data/vc.json", "r", encoding="utf-8") as f:
    vocabulario = json.load(f)

# === 2. Criar cliente Chroma (persistente) ===
client = chromadb.PersistentClient(path="db_vocabulario")
collection = client.get_or_create_collection("vocabulario")


for i, item in enumerate(vocabulario):
    texto = f"{item['term']}: {item['definition']}"
    collection.add(ids=[str(i)],
                    documents=[texto],
                    metadatas=[{
                        "term": item["term"]
                    }])
print(f"✅ {len(vocabulario)} termos adicionados ao banco vetorial.")

def adicionar_termo(term, definition):
    novo_id = str(collection.count() + 1)
    collection.add(ids=[novo_id],
                   documents=[f"{term}: {definition}"],
                   metadatas=[{
                       "term": term
                   }])
    print(f"➕ Termo '{term}' adicionado com sucesso!")

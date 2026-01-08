# build_index.py
import json
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

VOCAB_PATH = "../data/vc.json"
INDEX_PATH = "vectorstore/vocab_index"

# === Carrega vocabulário ===
with open(VOCAB_PATH, encoding="utf-8") as f:
    vocab = json.load(f)

# === Constrói documentos ===
docs = []
for item in vocab:
    text = f"{item['term']}. {item['definition']}"
    docs.append(
        Document(
            page_content=text,
            metadata={"term": item["term"]}
        )
    )

# === Embeddings (Ollama) ===
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)

# === Cria índice vetorial ===
db = FAISS.from_documents(docs, embeddings)

# === Persiste em disco ===
db.save_local(INDEX_PATH)

print(f"Vocabulário indexado com {len(docs)} termos.")

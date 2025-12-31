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
def responder(question, modelo="llama3.2"):
    resultados = collection.query(query_texts=[question], n_results=300)
    contextos = "\n\n".join(resultados["documents"][0])

    prompt = f"""
Context:
You are an expert just in the field of Artificial Intelligence and works for a research institution.
You can speak many different languages.
However, you always answer in English. It doesn't matter which language the question is asked in.
Objective:
Extract terms, including acronyms, for indexing from a natural language question, ensuring terminological accuracy, traceability, and reproducibility, as required in scientific environments.
Mandatory restrictions:
The terms must be included in the vocabulary provided. (example.: thesaurus, ontology, scientific taxonomy).
The terms must appear explicitly in the question, with literal correspondence (string match).
Do not imply, infer, or deduce any terms beyond those explicitly stated in the question.
Do not use synonyms, morphological variations, lemmatization, translation or semantic inference.
Ignore stopwords and conjunctions.
If no term from the vocabulary is present in the question, return an empty list.
Output format:
Return exclusively a JSON list.
Maintain the exact spelling as defined in the controlled vocabulary.
Do not include metadata, justifications or explanatory text after the response.

VOCABULARY:
{contextos}

QUESTION: {question}

ANSWER:
"""
    

    resposta = ollama.chat(
        model=modelo,
        options={"temperature": 0.1},  # 👈 Aqui está o ajuste
        messages=[{
            "role": "user",
            "content": prompt
        }])

    content = resposta["message"]["content"]
    print("\n🧩 Question:", question)
    print("💬 Answer:", content)
    return content


# === 5. Teste ===
responder("Name a chatbot similar to Google BARD.")
responder("What is Big Data?")
responder("What is A3t-Gcn?")
responder("Define Abusive Language Detection.")
responder("What is the Abstractive Model present in AI?")
responder("Explain AI Authorship?")

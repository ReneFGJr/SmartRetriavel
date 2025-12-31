import json
import chromadb
import ollama

# === 1. Carregar vocabulário JSON ===
with open("data/vc.json", "r", encoding="utf-8") as f:
    vocabulario = json.load(f)

# === 2. Criar cliente Chroma (persistente) ===
client = chromadb.PersistentClient(path="db_vocabulario")
collection = client.get_or_create_collection("vocabulary")
# === 4. Função para responder ===
def responder(question, modelo="llama3.2"):
    resultados = collection.query(query_texts=[question], n_results=300)
    contextos = "\n\n".join(resultados["documents"][0])

    prompt = f"""
Context:
You are an expert just in the field of Artificial Intelligence.
You can speak many different languages.
However, you always give answers in English. It doesn't matter which language the question is asked in.

Objective:
Extract terms from the QUESTION, including acronyms, for indexing from natural language questions presented, ensuring terminological accuracy, traceability, and reproducibility, as required in scientific environments.

Mandatory restrictions:
The terms must be included in the vector database provided. (example.: thesaurus, ontology, scientific taxonomy).
The terms must appear explicitly in the QUESTION, with literal correspondence (string match).
Do not use synonyms, morphological variations, lemmatization, translation or semantic inference.
Ignore stopwords and conjunctions.
If no term from the vector database is present in the QUESTION, return an empty result in that specific case.
Output format:
Return exclusively a JSON list.
Return exclusively the terms found. In case they are not in english, translate them to english.
Maintain the exact spelling as defined in the vector database.
Do not include metadata, justifications or explanatory text after the response.
Do not imply, infer, or deduce any terms beyond those explicitly stated in the question.

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
responder("How a bias detection works?")

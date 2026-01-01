import json
import chromadb
import ollama

# === 1. Carregar vocabulário JSON ===
with open("data/vc.json", "r", encoding="utf-8") as f:
    vocabulary = json.load(f)

# === 2. Criar cliente Chroma (persistente) ===
client = chromadb.PersistentClient(path="db_vocabulario")
collection = client.get_or_create_collection("vocabulary")
# === 4. Função para responder ===
def responder(question, modelo="llama3.2"):
    resultados = collection.query(query_texts=[question], n_results=300)
    contextos = "\n\n".join(resultados["documents"][0])

    prompt = f"""

Context:   
You are an expert in the field of Artificial Intelligence.
You just talk about Artificial Intelligence.
You can speak many different languages.
However, you always give answers in English. It doesn't matter which language the question is asked in.
There is a VOCABULARY provided below, which contains terms and their definitions related to Artificial Intelligence.
And you just know the terms and the concepts presented in the VOCABULARY provided.

Objective:
To extract terms for indexing from a natural language query, ensuring terminological precision, traceability, and reproducibility, as required in scientific environments.

Mandatory constraints:
Terms must appear in the question, with literal matching (string match).
Terms must be present also in the provided controlled VOCABULARY (e.g., thesaurus, ontology, scientific taxonomy).


To aswer:
Do not use synonyms, morphological variations, lemmatization, translation, or semantic inference.
Ignore stopwords and connectives.
Ignore terms that are not related to the field of Artificial Intelligence.
If no term from the controlled VOCABULARY is present in the query, return an empty list.
Do not include metadata, justifications or explanatory text after the answer.

Preprocessing procedure:
Normalize the query (remove irrelevant punctuation). 
Tokenize the question into n-grams compatible with the VOCABULARY terms.
Perform an exact match between the n-grams in the question and the terms in the controlled VOCABULARY.
Validate each selected term for its literal presence in the question and in the VOCABULARY.

Answer format:
Return only a JSON list.
Maintain the exact spelling as defined in the controlled VOCABULARY.
Do not include justifications, or explanatory text

VOCABULARY:
{json}

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
responder("What is Bias Detection?")
responder("Quantos dedos eu tenho na mão?")

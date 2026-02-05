import json
import sys
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
However, when someone asks you a question or requests some information from you you always give answers in English. It doesn't matter what language the question/request is made in.
There is a VOCABULARY provided below, which contains terms (and their definitions) that belong to the field of Artificial Intelligence.
You must read and learn the terms and definitions presented in the VOCABULARY provided.

Objective:
To extract terms from the questions/sentences that are applied, ensuring terminological precision, traceability, and reproducibility, as required in scientific environments.
Present the terms in English.

Mandatory constraints for term extraction:
Terms must appear in the question/sentence.
Terms must also be present in the VOCABULARY provided, with literal matching (string match).

While extracting the terms:
Ignore stopwords and connectives.
Ignore terms that are not related to the field of Artificial Intelligence.
If no term from the VOCABULARY provided is presented in the question/sentence, return an empty list ([]).

Preprocessing procedure:
Validate each selected term for its literal presence in the question/sentence and in the VOCABULARY provided.

Answer format:
Return only a JSON list.
Maintain the exact spelling of the term as defined in the VOCABULARY provided.
Do not include metadata, justifications, explanatory text or any sort of note before or after the answers.
Do not replace terms with synonyms, morphological variations, lemmatization or semantic inferences.

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
responder("Name a chatbot similar to BARD.")
responder("What is Big Data?")
responder("What is A3t-GCN?")
responder("Define Abusive Language Detection.")
responder("What is the Abstractive Model present in Artificial Intelligence?")
responder("Explain Artificial Intelligence Authorship?")
responder("What is Bias Detection?")
responder("Quantos dedos eu tenho na mão?")
responder("A inteligência dele é muito superficial.")
responder("The Active Inference make use of AI.")

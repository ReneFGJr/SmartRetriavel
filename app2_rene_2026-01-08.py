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
    prompt = f"""

Role:
You are an expert in Artificial Intelligence terminology extraction.

Language policy:
You must always answer in English, regardless of the language of the input.

Task:
Extract terms from the QUESTION that meet ALL the following conditions:
1. The term must appear EXACTLY (literal string match) in the QUESTION.
2. The term must appear EXACTLY in the VOCABULARY.
3. The term must belong to the field of Artificial Intelligence.
4. Ignore stopwords, connectors, and explanatory phrases.
5. Do NOT infer, translate, lemmatize, pluralize, or use synonyms.
6. If no valid term is found, return an empty JSON list: [].

Validation:
For each extracted term, verify:
- Literal presence in the QUESTION
- Literal presence in the VOCABULARY

Output format:
- Return ONLY a JSON list
- No explanations, no metadata, no extra text

VOCABULARY:
Term: Abrobation
Definition: The substance that is used to abrobate or reduce the intensity of a signal in artificial intelligence systems, particularly in neural networks.

QUESTION: {question}
"""
    
    #print(prompt)

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
responder("What is Abrobation?")
responder("that is used to abrobate or reduce the intensity of a signal in artificial intelligence systems, particularly in neural networks.")
responder("O que é usado para atenuar ou reduzir a intensidade de um sinal em sistemas de inteligência artificial, particularmente em redes neurais.")
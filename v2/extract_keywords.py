# extract_keywords.py
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM

INDEX_PATH = "vectorstore/vocab_index"

# === Embeddings ===
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)

# === Carrega índice FAISS (seguro, criado localmente) ===
db = FAISS.load_local(
    INDEX_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# === LLM ===
llm = OllamaLLM(
    model="llama3.2",
    base_url="http://localhost:11434",
    temperature=0.1
)

def extract_keywords(text, k=8):
    # Busca semântica no vocabulário
    results = db.similarity_search(text, k=k)
    terms = [r.metadata["term"] for r in results]

    prompt = f"""
You are an expert in Knowledge Organization.

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

Text:
{text}

Candidate terms:
{terms}

Return only a list of normalized keywords,
in English, in JSON format.
"""

    response = llm.invoke(prompt)
    return response.strip()

if __name__ == "__main__":
    texto_pesquisa = """
    Uso de inteligência artificial para apoiar revisões sistemáticas
    da literatura científica em bibliotecas digitais.
    """

    keywords = extract_keywords(texto_pesquisa)
    print("Palavras-chave sugeridas:")
    print(keywords)

    print("=======================")
    print(extract_keywords("Qual ao melhor técnica para analisar grandes coleções de textos"))

    print("=======================")
    print(extract_keywords("Automatic indexing using AI in full text. Identify outliers in large datasets."))

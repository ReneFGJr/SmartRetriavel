import json
import requests
import unicodedata
import re
from difflib import get_close_matches

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


# ========= Normalização =========
def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


# ========= Carregar vocabulário =========
def load_authorized_terms(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    terms = []
    for entry in data:
        for term, lang in entry.items():
            #if lang == "por":
            terms.append(term)
    return terms


# ========= Chamada ao Ollama =========
def ollama_interpret(question: str):
    prompt = f"""
Você é um sistema de apoio à indexação controlada.

Regras:
- Identifique APENAS conceitos centrais
- NÃO explique
- NÃO use frases completas
- NÃO invente termos
- Retorne APENAS termos conceituais curtos, separados por vírgula

Pergunta:
{question}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "top_p": 0.1,
            "seed": 42
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )
    response.raise_for_status()

    text = response.json()["response"]
    concepts = [c.strip() for c in text.split(",") if c.strip()]
    return concepts


# ========= Alinhamento com vocabulário =========
def align_with_vocabulary(concepts, authorized_terms, cutoff=0.70):
    normalized_vocab = {normalize(t): t for t in authorized_terms}
    matched_terms = set()

    for concept in concepts:
        norm_concept = normalize(concept)
        matches = get_close_matches(
            norm_concept,
            normalized_vocab.keys(),
            n=3,
            cutoff=cutoff
        )
        for m in matches:
            matched_terms.add(normalized_vocab[m])

    return sorted(matched_terms)


# ========= Função principal RAG =========
def rag_query(question: str, json_path: str):
    authorized_terms = load_authorized_terms(json_path)

    llm_concepts = ollama_interpret(question)
    aligned_terms = align_with_vocabulary(llm_concepts, authorized_terms)

    return {
        "pergunta_original": question,
        "conceitos_interpretados_pelo_llm": llm_concepts,
        "termos_autorizados_alinhados": aligned_terms,
        "modelo_llm": "llama3.2 (Ollama)",
        "fonte_vocabulario": "por.json"
    }


# ========= Execução =========
if __name__ == "__main__":
    pergunta = "Como a IAG é utilizada na catalogação de livros?"
    resultado = rag_query(pergunta, "data/por.json")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

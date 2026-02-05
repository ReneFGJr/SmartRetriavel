import json
import unicodedata
import re
from difflib import get_close_matches

# ========= 1. Normalização =========
def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


# ========= 2. Carregar termos autorizados =========
def load_authorized_terms(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    authorized_terms = []

    for entry in data:
        for term, lang in entry.items():
            if lang == "por":
                authorized_terms.append(term)

    return authorized_terms


# ========= 3. Extração de palavras-chave =========
def extract_keywords(question: str):
    question = normalize(question)
    tokens = re.findall(r"\b[a-záéíóúãõç]{3,}\b", question)
    return list(set(tokens))


# ========= 4. Alinhamento semântico =========
def align_terms(keywords, authorized_terms, cutoff=0.75):
    normalized_terms = {normalize(t): t for t in authorized_terms}
    matches = set()

    for kw in keywords:
        close = get_close_matches(
            kw,
            normalized_terms.keys(),
            n=3,
            cutoff=cutoff
        )
        for c in close:
            matches.add(normalized_terms[c])

    return sorted(matches)


# ========= 5. Função principal =========
def rag_query(question: str, json_path: str):
    authorized_terms = load_authorized_terms(json_path)
    keywords = extract_keywords(question)
    aligned_terms = align_terms(keywords, authorized_terms)

    return {
        "pergunta_original": question,
        "palavras_chave_extraidas": keywords,
        "termos_autorizados_identificados": aligned_terms,
        "fonte_vocabulario": "por.json"
    }


# ========= 6. Exemplo de uso =========
if __name__ == "__main__":
    pergunta = "Como a inteligência artificial é utilizada em bibliotecas?"
    resultado = rag_query(pergunta, "data/por.json")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

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
def responder(pergunta, modelo="llama3.2"):
    resultados = collection.query(query_texts=[pergunta], n_results=3)
    contextos = "\n\n".join(resultados["documents"][0])

    prompt = f"""
Você é um especialista em acessibilidade e organização do conhecimento.
Use o vocabulário abaixo para responder à pergunta do usuário.
Extraia as palavras-chave do PERGUNTA.
Utilize somente os termos do vocabulário fornecido.
Responda somente os termos no formato JSON, sem comentários.
Mostre somente as sem as chaves do JSON.

VOCABULÁRIO:
{contextos}

PERGUNTA: {pergunta}

RESPOSTA:
"""

    resposta = ollama.chat(
        model=modelo,
        options={"temperature": 0.1},  # 👈 Aqui está o ajuste
        messages=[{
            "role": "user",
            "content": prompt
        }])

    conteudo = resposta["message"]["content"]
    print("\n🧩 Pergunta:", pergunta)
    print("💬 Resposta:", conteudo)
    return conteudo


# === 5. Teste ===
responder("Quais são as barreiras de acesso em bibliotecas públicas?")
responder("Como a biblioteconomia se relaciona com a Inteligência Artificial?")
responder("Quais são os principais desafios para a inclusão digital de pessoas com deficiência?")
responder("Quais autores fundamentam a acessibilidade na informação ?")
responder("Quais são as melhores práticas para organizar um vocabulário controlado em bibliotecas digitais?")
responder("Acesso ao cadeirante")
responder("Melhor base de dados para biblioteconomia")
responder("Melhore vocabulário controlado em biblioteca digitai")
responder("quem criou a brapci")
responder("Editora Universitária")

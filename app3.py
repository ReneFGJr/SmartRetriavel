import json
import chromadb
import ollama

# === 2. Criar cliente Chroma (persistente) ===
client = chromadb.PersistentClient(path="db_vocabulario")
collection = client.get_or_create_collection("vocabulario")


# === 4. Função para responder ===
def responder(pergunta, modelo="llama3.2", temperatura=0.1):
    resultados = collection.query(query_texts=[pergunta], n_results=3)
    contextos = "\n\n".join(resultados["documents"][0])

    prompt = f"""
Você é um especialista em acessibilidade e organização do conhecimento.
Extraia as palavras-chave do PERGUNTA.
Mostre somente as palavras-chave separadas por ponto e vírgula,sem comentários.
PERGUNTA: {pergunta}

RESPOSTA:
"""

    resposta = ollama.chat(
        model=modelo,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        options={"temperature": temperatura}  # 👈 Aqui está o ajuste
    )

    conteudo = resposta["message"]["content"]
    print("\n🧩 Pergunta:", pergunta)
    print("💬 Resposta:", conteudo)
    return conteudo


# === 5. Teste ===
#responder("Quais são as barreiras de acesso em bibliotecas públicas?")
#responder("Como a biblioteconomia se relaciona com a Inteligência Artificial?")
#responder("Quais são os principais desafios para a inclusão digital de pessoas com deficiência?")
#responder("Quais autores fundamentam a acessibilidade na informação ?")
#responder("Quais são as melhores práticas para organizar um vocabulário controlado em bibliotecas digitais?")
responder("Acesso ao cadeirante")
responder("Melhor base de dados para biblioteconomia")
responder("Melhore vocabulário controlado em biblioteca digitai")
responder("quem criou a brapci")
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
Contexto:
Você é um especialista em Inteligência Artificial.

Objetivo:
Extrair termos para indexação a partir de uma pergunta em linguagem natural, garantindo precisão terminológica, rastreabilidade e reprodutibilidade, conforme exigido em ambientes científicos.

Restrições obrigatórias:
Os termos devem constar no vocabulário controlado fornecido (ex.: tesauro, ontologia, taxonomia científica).
Os termos devem aparecer explicitamente na pergunta, com correspondência literal (string match).
Não utilizar sinônimos, variações morfológicas, lematização, tradução ou inferência semântica.
Ignorar stopwords e conectivos.
Caso nenhum termo do vocabulário controlado esteja presente na pergunta, retornar uma lista vazia.

Formato da saída:
Retornar exclusivamente uma lista JSON.
Manter a grafia exata conforme definida no vocabulário controlado.
Não incluir metadados, justificativas ou texto explicativo após a resposta.
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
responder("Cite um chatbot semelhante ao Google BARD.")
responder("O que é Big Data?")
responder("What is Big Data?")
responder("O que é A3t-Gcn")
responder("Defina Detecção de Linguagem Abusiva.")
responder("Quais são os Modelos Abstrativos presentes na IA?")


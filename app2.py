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
Você é um modelo de linguagem (LLaMA 3.2) integrado a um sistema de Retrieval-Augmented Generation (RAG), atuando como um módulo de pré-processamento para indexação científica.

Objetivo:
Extrair termos para indexação a partir de uma pergunta em linguagem natural, garantindo precisão terminológica, rastreabilidade e reprodutibilidade, conforme exigido em ambientes científicos.

Restrições obrigatórias:
Os termos devem constar no vocabulário controlado fornecido (ex.: tesauro, ontologia, taxonomia científica).
Os termos devem aparecer explicitamente na pergunta, com correspondência literal (string match).
Não utilizar sinônimos, variações morfológicas, lematização, tradução ou inferência semântica.
Ignorar stopwords, conectivos e termos genéricos não científicos.
Caso nenhum termo do vocabulário controlado esteja presente na pergunta, retornar uma lista vazia.

Procedimento de pré-processamento:
Normalizar a pergunta (remoção de pontuação irrelevante).
Tokenizar a pergunta em n-grams compatíveis com os termos do vocabulário.
Realizar correspondência exata entre os n-grams da pergunta e os termos do vocabulário controlado.
Validar cada termo selecionado quanto à presença literal na pergunta.

Formato da saída:
Retornar exclusivamente uma lista JSON.
Manter a grafia exata conforme definida no vocabulário controlado.
Não incluir metadados, justificativas ou texto explicativo.
Não incluir explicações de procedimento.
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
responder("Cite um chatbot semelhante ao BARD.")
responder("O que é Big Data?")
responder("What is Big Data?")
responder("Cite um método avançado de IA.")
responder("Defina Detecção de Linguagem abusiva.")
responder("Quais são os sistemas de IA?")


import ollama


# === Função principal de correção ===
def corrigir_texto_llm(texto, modelo="llama3.2"):
    """
    Usa um modelo de linguagem para corrigir erros de ortografia e gramática
    de forma contextual, simulando o comportamento do Google Search.
    """

    prompt = f"""
Você é um corretor ortográfico e gramatical especializado em português.
Corrija o Texto:
- Responda apenas com o texto corrigido, sem comentários ou explicações.

Texto: {texto}
"""

    resposta = ollama.chat(model=modelo,
                           messages=[{
                               "role": "user",
                               "content": prompt
                           }])

    return resposta["message"]["content"].strip()


# === Função que exibe estilo “Google” ===
def exibir_correcao_google(consulta, modelo="llama3.2"):
    correcao = corrigir_texto_llm(consulta, modelo=modelo)

    if correcao.lower() != consulta.lower():
        print(f"P: {correcao}")
        print(f"R: {consulta}")
    else:
        print(f"Exibindo resultados para: {consulta}")


# === Teste ===
if __name__ == "__main__":
    consulta_usuario = "analesie de inteligenxia atifial"
    exibir_correcao_google(consulta_usuario)

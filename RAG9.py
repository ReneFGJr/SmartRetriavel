import mod_thesa_v2
import json

print("=== RAG com Vocabulário Controlado ===")

pergunta = "o que é RAG na IA"
resultado = mod_thesa_v2.rag_query(pergunta, "data/por.json")
print(json.dumps(resultado, ensure_ascii=False, indent=2))

pergunta = "Como a RAG é utilizada a Augmentação?"
resultado = mod_thesa_v2.rag_query(pergunta, "data/por.json")
print(json.dumps(resultado, ensure_ascii=False, indent=2))

import string
import unicodedata
import re
import smith_waterman

voc_file="data/vc_words_6.vc"
print("Inicializando bibliotecas...")
#with open(voc_file, "r", encoding="utf-8") as f:
#vocabulario = [linha.strip() for linha in f if linha.strip()]
with open(voc_file, "r", encoding="utf-8") as f:
    lista = [linha.strip() for linha in f if linha.strip()]

#******************************************************* Normalização
def normalizar(texto):
    """Remove acentos, coloca em minúsculas e limpa espaços extras."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9áéíóúãõç\s-]", "", texto)
    return texto

#***************************************************************/
def corrigir_palavra(palavra, vocabulario):
    melhor_palavra = None
    melhor_score = -1
    
    for voc in vocabulario:
        score = smith_waterman(palavra, voc)
        if score > melhor_score:
            melhor_score = score
            melhor_palavra = voc
    
    return melhor_palavra

#***************************************************************/
def word(w:string):
    w = w.lower().strip(string.punctuation + string.whitespace)

    print(w)
    return w
    
    
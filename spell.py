import mod_word

def palavras(palavra, vc):

    words = palavra.split()
    wordv = words.copy()

    i = 0
    for w in words:
        resultado = mod_word.existe_palavra(w, f"data/vc_words_{vc}.vc")
        if resultado:
            wordv[i] = True
        else:
            wordv[i] = False
        i += 1



if __name__ == "__main__":
    palavra = "analesie de inteligenxia atifial"
    vc = "6"
    palavras(palavra, vc)
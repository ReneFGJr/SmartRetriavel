import mod_word
import mod_smart_words

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
    print(words)
    print(wordv)


if __name__ == "__main__":
    palavra = "analesie de inteligenxia atifial"
    vc = "6"
    print(palavra)
    print(palavras(palavra, vc))
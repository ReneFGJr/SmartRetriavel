from itertools import permutations
import unicodedata
import re
import os

def existe_palavra(palavra, voc_file="data/vc_words_6.vc"):
    """Verifica se a palavra existe no vocabulário."""
    palavra = normalizar(palavra)

    if not os.path.exists(voc_file):
        raise FileNotFoundError(
            f"Arquivo de vocabulário não encontrado: {voc_file}")

    with open(voc_file, "r", encoding="utf-8") as f:
        vocabulario = [linha.strip() for linha in f if linha.strip()]

    return palavra in vocabulario

def verificar_palavra_inteligente(palavra,
                                  voc_file="data/vc_words_6.vc",
                                  max_distancia=2,
                                  max_diff_len=3):
    """
    Verifica se a palavra existe no vocabulário.
    Regras:
    1️⃣ Verifica se o número de caracteres é próximo.
    2️⃣ Se sim, usa distância de Levenshtein (erros de digitação).
    3️⃣ Se não encontrar, tenta Soundex (similaridade fonética).
    """
    palavra = normalizar(palavra)

    if not os.path.exists(voc_file):
        raise FileNotFoundError(
            f"Arquivo de vocabulário não encontrado: {voc_file}")

    with open(voc_file, "r", encoding="utf-8") as f:
        vocabulario = [linha.strip() for linha in f if linha.strip()]

    # === 1️⃣ Verifica existência exata ===
    if palavra in vocabulario:
        print(f"✅ '{palavra}' encontrado no vocabulário.")
        return palavra

    # === 2️⃣ Função auxiliar: distância de Levenshtein ===
    def distancia_levenshtein(a, b):
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                custo = 0 if a[i - 1] == b[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1,
                               dp[i - 1][j - 1] + custo)
        return dp[m][n]

    # === 3️⃣ Função auxiliar: Soundex simplificado ===
    def soundex_portugues(palavra):
        palavra = normalizar(palavra)
        if not palavra:
            return ""
        mapa = {
            "b": "1",
            "f": "1",
            "p": "1",
            "v": "1",
            "c": "2",
            "g": "2",
            "j": "2",
            "k": "2",
            "q": "2",
            "s": "2",
            "x": "2",
            "z": "2",
            "d": "3",
            "t": "3",
            "l": "4",
            "m": "5",
            "n": "5",
            "r": "6"
        }
        primeira = palavra[0].upper()
        codigos = [mapa.get(letra, "") for letra in palavra[1:]]
        codigo = [primeira]
        for c in codigos:
            if not codigo or c != codigo[-1]:
                codigo.append(c)
        codigo = "".join(codigo)
        codigo = (codigo + "0000")[:4]
        return codigo

    palavra_soundex = soundex_portugues(palavra)

    melhor_match = None
    menor_dist = 999
    melhor_fonetico = None

    for termo in vocabulario:
        # === Regra 1: diferença de tamanho ===
        if abs(len(palavra) - len(termo)) > max_diff_len:
            continue

        # === Regra 2: distância de Levenshtein ===
        dist = distancia_levenshtein(palavra, termo)
        if dist < menor_dist:
            menor_dist = dist
            melhor_match = termo

        # === Regra 3: fonética ===
        if soundex_portugues(termo) == palavra_soundex:
            melhor_fonetico = termo

    # === Resultado ===
    if menor_dist <= max_distancia:
        print(
            f"❓ '{palavra}' não encontrado. Palavra mais próxima: '{melhor_match}' (distância {menor_dist})"
        )
        return melhor_match
    elif melhor_fonetico:
        print(
            f"🔊 '{palavra}' não encontrado. Palavra mais próxima (fonética): '{melhor_fonetico}'"
        )
        return melhor_fonetico
    else:
        print(f"❌ '{palavra}' não encontrado e sem similaridade próxima.")
        return None


def gerar_permutacoes(palavra, arquivo_vocab):
    """
    Gera permutações da palavra e retorna apenas as que existem no arquivo de vocabulário.

    :param palavra: string original (ex: 'bias')
    :param arquivo_vocab: caminho do arquivo de vocabulário (ex: 'data/vc_words_6.vc')
    :return: lista de permutações existentes
    """
    # 🔹 Carregar o vocabulário (uma palavra por linha)
    with open(arquivo_vocab, 'r', encoding='utf-8') as f:
        vocab = set([linha.strip().lower() for linha in f if linha.strip()])

    print(f"📚 Vocabulário carregado com {len(vocab)} palavras.")
    print(f"🔤 Gerando permutações para a palavra: {palavra}")

    # 🔹 Criar todas as permutações possíveis da palavra
    permutacoes = [''.join(p) for p in permutations(palavra)]
    print(f"🧩 Total de permutações geradas: {len(permutacoes)}")

    # 🔹 Filtrar apenas as que estão no vocabulário
    encontradas = [p for p in permutacoes if p.lower() in vocab]

    print(f"✅ {len(encontradas)} permutações encontradas no vocabulário.")
    return encontradas


# === Normalização ===
def normalizar(texto):
    """Remove acentos, coloca em minúsculas e limpa espaços extras."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9áéíóúãõç\s-]", "", texto)
    return texto

# === Execução direta ===
if __name__ == "__main__":
    # === Exemplo de uso ===
    palavra = "modela"
    #palavra = "bais"
    palavra = "behavor"
    resultado = gerar_permutacoes(palavra, "data/vc_words_6.vc")

    print(f"🔤 Palavra: {palavra}")
    print(f"🧩 Total de combinações: {len(resultado)}")
    print("📜 Algumas combinações:")
    print(resultado[:10])  # Mostra apenas as 10 primeiras

    for n in resultado:
        term = verificar_palavra_inteligente(n)
        print(f"🔍 Verificando '{n}' -> Resultado: {term}")
        if term is not None:
            break

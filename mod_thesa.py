# ===============================================================
# Módulo: mod_thesa.py
# Função: Verificar se palavra existe ou sugerir similar no vocabulário
# Autor: René Faustino Gabriel Junior (adaptado por GPT-5)
# ===============================================================

import json
import sys
import unicodedata
import os
import re
import requests
from difflib import SequenceMatcher
from itertools import permutations


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


# === Gera vocabulário .vc ===
def processar_json(json_text, id="local"):
    """Lê JSON do Thesa e gera vocabulário controlado (.vc)."""
    data = json.loads(json_text)
    termos_data = data.get("terms", [])
    termos = set()

    for item in termos_data:
        termo = item.get("Term")
        if termo:
            termos.add(normalizar(termo))

    os.makedirs("data", exist_ok=True)
    output_file = f"data/vc_{id}.vc"

    termos_ordenados = sorted(termos)
    with open(output_file, "w", encoding="utf-8") as f:
        for termo in termos_ordenados:
            f.write(termo + "\n")

    print(
        f"💾 Arquivo '{output_file}' criado com {len(termos_ordenados)} termos."
    )
    return output_file


# === Extrai palavras únicas ===
def extrair_sintagmas(input_file, id="local"):
    """Gera lista de palavras únicas a partir de um vocabulário."""
    palavras = set()
    with open(input_file, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            tokens = re.split(r"[\s\-]+", linha)
            for token in tokens:
                token = normalizar(token)
                if len(token) > 2:
                    palavras.add(token)

    output_file = f"data/vc_words_{id}.vc"
    with open(output_file, "w", encoding="utf-8") as f:
        for p in sorted(palavras):
            f.write(p + "\n")

    print(
        f"💾 Arquivo '{output_file}' criado com {len(palavras)} palavras únicas."
    )
    return output_file


def distancia_levenshtein(a, b):
    """Calcula a distância de Levenshtein entre duas palavras."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            custo = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # remoção
                dp[i][j - 1] + 1,  # inserção
                dp[i - 1][j - 1] + custo  # substituição
            )

    return dp[m][n]

def verificar_palavra(palavras):
    print("🔤 Palavra:", palavras)
    wordsX = gerar_permutacoes(palavras)
    print(wordsX)
    sys.exit()

def verificar_palavra_busca(palavra, voc_file="data/vc_words_6.vc", max_distancia=5):
    """
    Verifica se a palavra existe no vocabulário.
    Se não existir, procura similar com distância de Levenshtein <= max_distancia.
    """
    palavra = normalizar(palavra)

    if not os.path.exists(voc_file):
        raise FileNotFoundError(
            f"Arquivo de vocabulário não encontrado: {voc_file}")

    with open(voc_file, "r", encoding="utf-8") as f:
        vocabulario = [linha.strip() for linha in f if linha.strip()]

    # 1️⃣ Verifica existência exata
    if palavra in vocabulario:
        print(f"✅ '{palavra}' encontrado no vocabulário.")
        return palavra

    # 2️⃣ Busca palavra mais próxima
    melhor_match = None
    menor_dist = 9999

    for termo in vocabulario:
        dist = distancia_levenshtein(palavra, termo)
        if dist < menor_dist:
            menor_dist = dist
            melhor_match = termo

    if menor_dist <= max_distancia:
        print(
            f"❓ '{palavra}' não encontrado. Palavra mais próxima: '{melhor_match}' (distância {menor_dist})"
        )
        return melhor_match
    else:
        print(f"❌ '{palavra}' não encontrado e sem similaridade próxima.")
        return None


def soundex_portugues(palavra):
    """Gera código Soundex simplificado adaptado ao português."""
    palavra = normalizar(palavra)
    if not palavra:
        return ""

    # Mapeamento fonético básico
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


# === Execução direta ===
if __name__ == "__main__":
    print("📁 Diretório atual:", os.getcwd())

    url = "https://www.ufrgs.br/thesa/api/terms/6"
    print(f"🔗 Acessando: {url}")
    response = requests.get(url)

    if response.status_code == 200:
        text = response.text
        vc_file = processar_json(text, id="6")
        extrair_sintagmas(vc_file, id="6")

        # 🔎 Testes de verificação
        verificar_palavra("inteligencia")  # existe
        verificar_palavra("intelgencia")  # erro de digitação
        verificar_palavra("inteligencio")  # pequeno erro
        verificar_palavra("ChatGTP")  # similar
        verificar_palavra("chatFTP")  # pode ou não existir
        verificar_palavra("bais")  # pode ou não existir
        verificar_palavra_inteligente("bais")  # pode ou não existir

    else:
        print(f"❌ Erro ao acessar a URL: {response.status_code}")

    # === Exemplo de uso ===
    palavra = "bias"
    resultado = gerar_permutacoes(palavra)

    print(f"🔤 Palavra: {palavra}")
    print(f"🧩 Total de combinações: {len(resultado)}")
    print("📜 Algumas combinações:")
    print(resultado[:10])  # Mostra apenas as 10 primeiras

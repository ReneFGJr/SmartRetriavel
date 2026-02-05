import json
import requests
from pathlib import Path


def download_json(url: str, output_file: str) -> None:
    """
    Faz o download de uma URL que retorna JSON
    e salva o conteúdo em um arquivo .json

    :param url: URL da API
    :param output_file: caminho do arquivo JSON de saída
    """

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # erro HTTP (404, 500, etc.)

        # Converte resposta para JSON
        data = response.json()

        # Garante que o diretório existe
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Salva em arquivo JSON formatado
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Arquivo salvo com sucesso em: {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")

    except json.JSONDecodeError:
        print("Erro: a resposta não é um JSON válido")

import json
from pathlib import Path
from typing import List, Dict

def gerar_contexto_vc_json(

) -> None:
    print("OK")

def gerar_contexto_vc(
    input_json: str,
    output_txt: str,
    fonte: str = "Vocabulário Controlado – Thesa / UFRGS"
) -> None:
    """
    Gera um arquivo de contexto textual a partir de um vocabulário controlado em JSON,
    seguindo boas práticas para uso em RAG e LLMs (modelo Brapci).

    :param input_json: caminho do arquivo vc.json
    :param output_txt: caminho do arquivo de contexto final (.txt)
    :param fonte: fonte institucional do vocabulário
    """

    input_path = Path(input_json)
    output_path = Path(output_txt)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8") as f:
        dados: List[Dict] = json.load(f)

    blocos = []

    for item in dados:
        termo = item.get("term", "").strip()
        definicoes = item.get("definition", [])

        if not termo or not definicoes:
            continue

        # Prioriza definição em português (heurística simples)
        definicao_pt = next(
            (d for d in definicoes if any(p in d.lower() for p in [" é ", " são ", " refere-se", "utiliza"])),
            definicoes[0]
        )

        definicao_pt = " ".join(definicao_pt.split())

        bloco = f"""[CONCEITO]
[TERMO]: {termo}

[DEFINIÇÃO]:
{definicao_pt}
"""
        blocos.append(bloco)

    contexto_final = "\n".join(blocos)

    with output_path.open("w", encoding="utf-8") as f:
        f.write(contexto_final)

    print(f"✅ Contexto gerado com sucesso em: {output_path}")

from pathlib import Path


def carregar_contexto(path_contexto: str) -> str:
    """
    Lê um arquivo de texto de contexto e retorna seu conteúdo como string.
    Ideal para uso como contexto em Ollama / RAG.

    :param path_contexto: caminho do arquivo de contexto (.txt)
    :return: conteúdo do arquivo como string
    """
    contexto_path = Path(path_contexto)

    if not contexto_path.exists():
        raise FileNotFoundError(f"Arquivo de contexto não encontrado: {contexto_path}")

    with contexto_path.open("r", encoding="utf-8") as f:
        return f.read().strip()


if __name__ == "__main__":
    url = "https://www.ufrgs.br/thesa/api/ai_rag_json/6/por"
    arquivo_saida = "data/vc.json"

    download_json(url, arquivo_saida)

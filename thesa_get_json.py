import json
import requests


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

        # Salva em arquivo JSON formatado
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Arquivo salvo com sucesso em: {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")

    except json.JSONDecodeError:
        print("Erro: a resposta não é um JSON válido")

if __name__ == "__main__":
    url = "https://www.ufrgs.br/thesa/api/ai_rad_json/6"
    arquivo_saida = "data/vc.json"

    download_json(url, arquivo_saida)
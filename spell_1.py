import difflib

# Dicionário de palavras conhecidas
dicionario = [
    "análise", "inteligência", "artificial", "dados", "ciência",
    "computacional"
]


def corrigir_consulta(texto):
    palavras = texto.split()
    corrigidas = []

    for palavra in palavras:
        sugestao = difflib.get_close_matches(palavra,
                                             dicionario,
                                             n=1,
                                             cutoff=0.7)
        if sugestao:
            corrigidas.append(sugestao[0])
        else:
            corrigidas.append(palavra)
    return " ".join(corrigidas)


consulta = "analesie de inteligencia atifial"
print("🔍 Você quis dizer:", '\n', consulta, '\n', corrigir_consulta(consulta))

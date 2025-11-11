import symspellpy
from symspellpy import SymSpell, Verbosity

# Inicializar
sym_spell = SymSpell(max_dictionary_edit_distance=2)
sym_spell.load_dictionary("pt_br_words.txt", 0,
                          1)  # Arquivo de palavras e frequência

# Corrigir
entrada = "analesie de inteligencia atifial"
suggestions = sym_spell.lookup_compound(entrada, max_edit_distance=2)

print("🔍 ", entrada)
print("🔍 ", suggestions[0].term)

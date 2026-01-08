import json
import sys
import chromadb
import ollama
from typer import prompt

# ============================================================
# 1. Load the controlled vocabulary from a JSON file
#    The vocabulary is expected to be a list of dictionaries
#    with the keys: "term" and "definition"
# ============================================================
with open("data/vc.json", "r", encoding="utf-8") as f:
    vocabulary = json.load(f)


def format_terms_from_json(data):
    """
    Convert a vocabulary JSON structure into a formatted text block.

    Parameters
    ----------
    data : list of dict
        Each dictionary must contain:
        - 'term': the controlled term (string)
        - 'definition': a string or a list of definition strings

    Returns
    -------
    str
        A single string where each term is formatted as:

        Term: <term>
        Definition: <definition>

        Multiple terms are separated by a blank line.
    """

    output = []

    for item in data:
        # Extract and normalize the term
        term = item.get("term", "").strip()

        # Definitions may be provided as a list or a single string
        # If it is a list, join all definition fragments into one text
        definition = item.get("definition", [])
        if isinstance(definition, list):
            definition = " ".join(d.strip() for d in definition)
        else:
            definition = str(definition).strip()

        # Standardized output format expected by the LLM prompt
        formatted_text = f"Term: {term}\nDefinition: {definition}"
        output.append(formatted_text)

    return "\n\n".join(output)


# Informational log to confirm vocabulary loading
print(f"Vocabulary successfully loaded with {len(vocabulary)} terms.")


# ============================================================
# 4. Main function responsible for querying the LLM
#    for terminology extraction based on a strict protocol
# ============================================================
def responder(question, modelo="phi4"):
    """
    Send a terminology-extraction task to an Ollama LLM.

    The model is instructed to extract ONLY those terms that:
    - Appear literally in the QUESTION
    - Appear literally in the VOCABULARY
    - Belong to the Artificial Intelligence domain

    Parameters
    ----------
    question : str
        The input question or sentence to be analyzed.
    modelo : str, optional
        The Ollama model name (default is 'llama3.2').

    Returns
    -------
    str
        The raw model response (expected to be a JSON list).
    """

    # Convert the full vocabulary into a textual context block
    contextos = format_terms_from_json(vocabulary)

    # Prompt explicitly enforces:
    # - Literal string matching
    # - No semantic inference
    # - Deterministic JSON-only output
    prompt = f"""

VOCABULARY:
{contextos}

Role:
You are an expert in Artificial Intelligence terminology extraction.

Language policy:
You must always answer in English, regardless of the language of the input.

Task:
Extract terms from the QUESTION that meet ALL the following conditions:
1. The term must appear EXACTLY (literal string match) in the QUESTION.
2. The term must appear EXACTLY in the VOCABULARY.
3. The term must belong to the field of Artificial Intelligence.
4. Ignore stopwords, connectors, and explanatory phrases.
5. Do NOT infer, translate, lemmatize, pluralize, or use synonyms.
6. If no valid term is found, return an empty JSON list: [].

Validation:
For each extracted term, verify:
- Literal presence in the QUESTION
- Literal presence in the VOCABULARY

Output format:
- Return ONLY a JSON list
- No explanations, no metadata, no extra text

QUESTION: {question}
"""

    # Optional debug output: shows the full prompt sent to the model
    #print(prompt)

    # Call the Ollama chat API with low temperature to reduce hallucinations
    resposta = ollama.chat(
        model=modelo,
        options={"temperature": 0.1},  # Low temperature for deterministic output
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    # Extract the model's textual response
    content = resposta["message"]["content"]

    # Display question and answer for traceability
    print("\n🧩 Question:", question)
    print("💬 Answer:", content)

    return content


# ============================================================
# 5. Test cases
#    These examples validate literal matching behavior
#    across definition-style, paraphrased, and translated inputs
# ============================================================
responder("Name a chatbot similar to BARD.")
responder("What is Big Data ?")
responder("How I can use massive, complex datasets ?")
responder("What is A3t-GCN ?")
responder("Define Abusive Language Detection.")
responder("What is the Abstract Model present in Artificial Intelligence?")
responder("Explain Artificial Intelligence Authorship?")
responder("What is Bias Detection?")
responder("Quantos dedos eu tenho na mão?")
responder("A inteligência dele é muito superficial.")
responder("The Active Inference make use of AI.")
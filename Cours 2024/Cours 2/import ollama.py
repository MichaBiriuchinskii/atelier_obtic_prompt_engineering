import ollama

def call_ollama(prompt: str, temperature: float = 0.1):
    """
    Appelle un modèle local via Ollama et retourne la réponse.

    Args:
        prompt: Le texte d'entrée
        temperature: Niveau de créativité (0.1 = peu créatif, 1 = très créatif)

    Returns:
        La réponse du modèle (ex: 'llama3')
    """
    try:
        response = ollama.chat(
            model='llama3.2',  
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": temperature}
        )

        result = response.get("message", {}).get("content", "").strip()

        if result.startswith(prompt):
            result = result[len(prompt):].strip()

        return result

    except Exception as e:
        return f"Erreur: {e}"

prompt = """Salut, ça va ? 
"""

response = call_ollama(prompt)

print(f"📜 Prompt: {prompt}")
print(f"📝 Réponse: {response}")

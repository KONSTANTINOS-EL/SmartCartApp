import requests

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_ai_for_recipe(product_name):
    ai = f"Δώσε μου μια απλή συνταγή που περιέχει το προϊόν: {product_name}. Να είναι Ελληνική συνταγή και να γράψεις τα υλικά και την διαδικασία της εκτέλεσης"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "user", "content": ai}
        ]
    }

    response = requests.post(GROQ_URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Σφάλμα AI: {response.status_code}"
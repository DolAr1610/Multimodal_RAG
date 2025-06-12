import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_response(question, retrieved_docs, model="meta-llama/llama-3-8b-instruct"):
    context = "\n\n".join(
        f"Title: {doc.get('title', 'N/A')}\n"
        f"Description: {doc.get('description', 'N/A')}\n"
        f"Content: {doc.get('content', 'N/A')}\n"
        for doc in retrieved_docs
    )

    prompt = (
        "You are a polite assistant who provides clear and detailed answers based solely on the information from The Batch articles.\n\n"
        "Rules:\n"
        "- Answer only using the knowledge from The Batch articles.\n"
        "- Do not mention other sources or questions; provide only accurate, detailed, and understandable answers.\n"
        "- If the information is present in the context, give a clear answer.\n"
        "- If the information is missing, respond with: 'Sorry, I could not find the answer in the provided context.'\n"
        "- Do not guess, fabricate information, or go beyond the given context.\n\n"
        f"Context for the answer:\n{context}"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
        "temperature": 0.3
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Помилка: {response.status_code} — {response.text}"

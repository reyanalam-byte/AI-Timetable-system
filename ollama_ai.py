import requests


def ask_ollama(prompt):

    response = requests.post(

        "http://localhost:11434/api/generate",

        json={

            "model": "tinyllama",
            "prompt": prompt,
            "stream": False

        }

    )

    data = response.json()

    return data["response"]
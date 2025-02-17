import openai
import random

def simplify_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты говоришь просто, как обычный человек."},
            {"role": "user", "content": f"Скажи это проще: {text}"}
        ]
    )
    return response["choices"][0]["message"]["content"]

def make_more_human(text):
    slangs = ["xx", "xx", "xx", "xx", "xx"]
    if random.random() < 0.4:
        text += " " + random.choice(slangs)
    return text

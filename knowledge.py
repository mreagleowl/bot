import os
import json
from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader

knowledge_base = []

def load_knowledge(directory="knowledge"):
    global knowledge_base
    if not os.path.exists(directory):
        os.makedirs(directory)

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if filename.endswith(".txt"):
            loader = TextLoader(filepath)
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(filepath)
        else:
            continue

        documents = loader.load()
        for doc in documents:
            knowledge_base.append(doc.page_content)

    with open("knowledge.json", "w", encoding="utf-8") as file:
        json.dump(knowledge_base, file, ensure_ascii=False, indent=4)

def search_knowledge(query):
    results = [text for text in knowledge_base if query.lower() in text.lower()]
    return results[:3] if results else ["Я пока не знаю этого 🤔"]

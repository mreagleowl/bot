import faiss
import numpy as np
import os
import json
from langchain.embeddings.openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

if os.path.exists("memory.index"):
    index = faiss.read_index("memory.index")
else:
    index = faiss.IndexFlatL2(1536)

if os.path.exists("memory.json"):
    with open("memory.json", "r", encoding="utf-8") as file:
        memory_data = json.load(file)
else:
    memory_data = []

def save_memory():
    with open("memory.json", "w", encoding="utf-8") as file:
        json.dump(memory_data, file, ensure_ascii=False, indent=4)
    faiss.write_index(index, "memory.index")

def add_to_memory(text):
    vector = np.array(embeddings.embed_query(text)).reshape(1, -1)
    index.add(vector)
    memory_data.append(text)
    save_memory()

def search_memory(query, top_k=3):
    vector = np.array(embeddings.embed_query(query)).reshape(1, -1)
    distances, indices = index.search(vector, top_k)
    results = [memory_data[i] for i in indices[0] if i < len(memory_data)]
    return results

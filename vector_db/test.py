import sys
sys.path.insert(0, "C:/Users/ADMIN/.gbt/vector_db")
from vector_db import VectorDB
import random, os

random.seed(42)
db = VectorDB()

docs = [
    "vector database stores and retrieves high-dim vectors",
    "machine learning uses embedding to convert text",
    "GBT xiaotudou is an all-in-one AI dev platform",
    "today weather is great for a walk in the park",
    "Python is an excellent programming language",
]
vecs = [[random.random() for _ in range(128)] for _ in range(5)]

db.insert("demo", vecs, texts=docs, doc_ids=[f"d{i}" for i in range(5)])

query = [random.random() for _ in range(128)]
r = db.search("demo", query, 3)

print(f"Total: {db.count('demo')} vectors")
print(f"Collections: {db.list_cols()}")
print(f"Search results:")
for did, txt, sim in r:
    print(f"  [{sim:.4f}] {txt}")

print(f"\nDB file: vectors.db")
print(f"Status: ALWAYS ON - zero server, zero disconnect!")

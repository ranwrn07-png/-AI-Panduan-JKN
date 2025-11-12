"""
Simple ingestion script: reads text files from ../docs and stores them in DB.
If OPENAI_API_KEY is set and USE_OPENAI_EMBEDDINGS=true in .env, will compute embeddings and save them.
"""
import os
from db import SessionLocal, init_db, Document
from dotenv import load_dotenv
import json

load_dotenv()
USE_OPENAI = os.getenv("USE_OPENAI_EMBEDDINGS", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def compute_embedding(text: str):
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        resp = openai.Embedding.create(model="text-embedding-3-small", input=text)
        return resp["data"][0]["embedding"]
    except Exception as e:
        print("Embedding failed or OpenAI not configured:", e)
        return None


def ingest_docs():
    init_db()
    db = SessionLocal()
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
    docs_dir = os.path.abspath(docs_dir)
    if not os.path.exists(docs_dir):
        print("No docs folder found at", docs_dir)
        return
    for fname in os.listdir(docs_dir):
        if not fname.lower().endswith(".txt"):
            continue
        path = os.path.join(docs_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        embedding = None
        if USE_OPENAI and OPENAI_API_KEY:
            embedding = compute_embedding(content)
        doc = Document(title=fname, content=content, embedding_json=json.dumps(embedding) if embedding else None)
        db.add(doc)
    db.commit()
    db.close()
    print("Ingest complete")

if __name__ == "__main__":
    ingest_docs()

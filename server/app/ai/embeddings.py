import os
from typing import List

provider = os.getenv("EMBEDDINGS_PROVIDER", "local")

# Lazy init to reduce cold start
_model = None

def _ensure_model():
    global _model
    if provider == "local":
        if _model is None:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        return _model
    elif provider == "openai":
        # no local model needed
        return None

async def embed_texts(texts: List[str]) -> List[List[float]]:
    if provider == "local":
        model = _ensure_model()
        return model.encode(texts, normalize_embeddings=True).tolist()
    elif provider == "openai":
        import os, httpx
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        url = "https://api.openai.com/v1/embeddings"
        model = "text-embedding-3-small"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, headers=headers, json={"model": model, "input": texts})
            resp.raise_for_status()
            data = resp.json()["data"]
            return [item["embedding"] for item in data]
    else:
        raise ValueError("Unsupported provider")
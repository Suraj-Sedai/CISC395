import os
import warnings
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

try:
    from huggingface_hub.utils import logging as hf_logging
except ImportError:  # pragma: no cover
    hf_logging = None

try:
    from transformers.utils import logging as transformers_logging
except ImportError:  # pragma: no cover
    transformers_logging = None

GUIDES_DIR = "guides"
DB_PATH = "chroma_db"
COLLECTION = "trip_guides"
CHUNK_SIZE = 200  # words
CHUNK_OVERLAP = 30  # words
MODEL_CACHE_DIR = ".hf_cache"

_MODEL = None


def _quiet_call(func, *args, **kwargs):
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        return func(*args, **kwargs)


def _get_model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        cache_dir = Path(MODEL_CACHE_DIR)
        cache_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("HF_HOME", str(cache_dir.resolve()))
        os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
        os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
        warnings.filterwarnings(
            "ignore",
            message=".*unauthenticated requests to the HF Hub.*",
        )
        if hf_logging is not None:
            hf_logging.set_verbosity_error()
        if transformers_logging is not None:
            transformers_logging.set_verbosity_error()
        _MODEL = _quiet_call(
            SentenceTransformer, "all-MiniLM-L6-v2", cache_folder=str(cache_dir)
        )
    return _MODEL


def read_file(path: str) -> str:
    file_path = Path(path)

    try:
        suffix = file_path.suffix.lower()
        if suffix in {".txt", ".md"}:
            text = file_path.read_text(encoding="utf-8")
        elif suffix == ".pdf":
            reader = PdfReader(str(file_path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            return ""
    except Exception as error:
        print(f"Warning: could not read {file_path.name}: {error}")
        return ""

    if not text.strip():
        print(f"Warning: {file_path.name} has no extractable text (scanned PDF?), skipping.")
        return ""

    return text


def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> list[str]:
    words = text.split()
    if not words:
        return []

    step = max(1, chunk_size - overlap)
    chunks = []

    for start in range(0, len(words), step):
        chunk = " ".join(words[start : start + chunk_size]).strip()
        if chunk:
            chunks.append(chunk)

    return chunks


def build_index(force: bool = False):
    guides_dir = Path(GUIDES_DIR)
    if not guides_dir.exists():
        print("Error: guides/ folder not found.")
        return

    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION)

    if force:
        existing_ids = collection.get(include=[])["ids"]
        if existing_ids:
            collection.delete(ids=existing_ids)

    supported_files = sorted(
        file_path
        for file_path in guides_dir.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in {".txt", ".md", ".pdf"}
    )

    if not supported_files:
        print("Warning: no supported files found in guides/.")
        return

    model = _get_model()
    total_chunks_added = 0
    indexed_files = 0

    existing_ids = set()
    if not force:
        existing_ids = set(collection.get(include=[])["ids"])

    for file_path in supported_files:
        text = read_file(str(file_path))
        if not text:
            continue

        chunks = chunk_text(text)
        if not chunks:
            continue

        indexed_files += 1

        ids_to_add = []
        docs_to_add = []

        for index, chunk in enumerate(chunks):
            chunk_id = f"{file_path.stem}_chunk_{index}"
            if not force and chunk_id in existing_ids:
                continue
            ids_to_add.append(chunk_id)
            docs_to_add.append(chunk)

        if not docs_to_add:
            continue

        embeddings = _quiet_call(model.encode, docs_to_add).tolist()
        collection.add(ids=ids_to_add, documents=docs_to_add, embeddings=embeddings)
        existing_ids.update(ids_to_add)
        total_chunks_added += len(docs_to_add)

    print(f"Indexed {total_chunks_added} chunks from {indexed_files} files.")


def ensure_index() -> object:
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION)

    if collection.count() == 0:
        print("No index found. Building from guides/...")
        build_index()
        collection = client.get_or_create_collection(name=COLLECTION)

    return collection


def search_guides(query: str, n_results: int = 3) -> list[str]:
    collection = ensure_index()
    if collection.count() == 0:
        return []

    model = _get_model()
    vector = _quiet_call(model.encode, query).tolist()
    n_results = min(n_results, collection.count())
    results = collection.query(query_embeddings=[vector], n_results=n_results)
    return results["documents"][0]


if __name__ == "__main__":
    build_index()

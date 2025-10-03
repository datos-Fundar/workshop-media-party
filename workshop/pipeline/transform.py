from workshop.utils.common import Metadata, Embedding
from workshop.utils.text_splitter import RecursiveCharacterSplitter
from workshop.utils.sentence_transformers import SentenceTransformer
from workshop.utils.cuda import is_cuda_available
import chromadb
import pathlib
from uuid import uuid4

def extraer_chunks(path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> tuple[list[str], list[Metadata], str]:
    splitter = RecursiveCharacterSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    path: pathlib.Path = pathlib.Path(path)

    chunks = list()
    metadatas = list()
    ids = list()

    for chunk in splitter.split_text(path.read_text()):
        metadatas.append(Metadata(path=str(path.resolve())).model_dump(mode='json', exclude_none=True))
        chunks.append(chunk)
        ids.append(str(uuid4()))
    
    return chunks, metadatas, ids

def vectorizar_textos(textos: list[str], modelo_embeddings: str = "sentence-transformers/all-mpnet-base-v2") -> list[Embedding]:
    try:
        modelo = SentenceTransformer(
            model_name_or_path=modelo_embeddings,
            device="cuda" if is_cuda_available() else "cpu",
            backend='torch',
        )
    except Exception:
        modelo = SentenceTransformer(
            model_name_or_path=modelo_embeddings,
            device="cpu",
            backend='torch',
        )
        print("No se pudo usar el GPU, se usará el CPU.")

    result: list[Embedding] = modelo.encode(textos, show_progress_bar=True)

    return result
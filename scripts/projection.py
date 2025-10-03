import chromadb
import rich
from workshop.utils.umap import UMAP
import numpy as np
from tqdm import tqdm

if __name__ == "__main__":
    coleccion = chromadb.PersistentClient().get_collection("argendata_topicos")
    resultado = coleccion.get(include=["metadatas", "documents", "embeddings"])

    ids = resultado['ids']
    embeddings = resultado['embeddings']
    chunks = resultado['documents']
    metadatas = resultado['metadatas']

    umap = UMAP(
            random_state=0,
            transform_seed=0,
        )
        
    chunk_ids = ids
    chunk_embeddings = embeddings
    chunk_embeddings = np.array(chunk_embeddings)

    umap_transform = umap.fit(chunk_embeddings)
    
    result = np.empty((len(chunks), 2))
    for i, chunk in enumerate(tqdm(chunks)):
        result[i] = umap_transform.transform([chunk_embeddings[i]]) # type: ignore[unsupported-operation]

    
    for i, metadata in enumerate(metadatas):
        metadata['projection_x'] = result[i][0]
        metadata['projection_y'] = result[i][1]

    coleccion.update(
        ids=ids,
        metadatas=metadatas,
    )

    metadatas = coleccion.get(include=["metadatas"])['metadatas']
    for metadata in metadatas:
        rich.print(metadata)

    
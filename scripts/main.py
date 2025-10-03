import pathlib
import workshop
import chromadb
from workshop.pipeline import (
    extraer_textos, 
    extraer_chunks, 
    vectorizar_textos, 
)

if __name__ == "__main__":
    dataset = workshop.dataset.argendata_topicos.download()
    procesados = pathlib.Path('./data/argendata_topicos/processed').glob('**/*.md')
    procesados = sorted(procesados)
    procesados = procesados[:]

    metadatas = list()
    chunks = list()
    ids = list()

    for procesado in procesados:
        chunks_doc, metadatas_doc, ids_doc = extraer_chunks(procesado, chunk_size=1000, chunk_overlap=200)
        
        chunks.extend(chunks_doc)
        metadatas.extend(metadatas_doc)
        ids.extend(ids_doc)
    
    nombre_coleccion = "argendata_topicos"

    db = chromadb.PersistentClient(path="chroma")

    colecciones_existentes = [c.name for c in db.list_collections()]

    if nombre_coleccion in colecciones_existentes:
        coleccion = db.get_collection(nombre_coleccion)
    else:
        vectores = vectorizar_textos(chunks)
        coleccion = db.create_collection(nombre_coleccion)
            
        coleccion.add(
            ids=ids,
            documents=chunks,
            embeddings=vectores,
            metadatas=metadatas,
        )
    
    resultado = coleccion.get(include=["metadatas", "documents", "embeddings"])
import chromadb
import rich
import altair as alt
import polars as pl
import pathlib
from workshop.utils.sentence_transformers import SentenceTransformer

if __name__ == "__main__":
    coleccion = chromadb.PersistentClient().get_collection("argendata_topicos")

    result = coleccion.get(include=["metadatas", "documents", "embeddings"])
    metadatas = result['metadatas']
    ids = result['ids']
    chunks = result['documents']
    embeddings = result['embeddings']

    df = pl.DataFrame([
        {
            'id': id,
            'chunk': f'{chunk[:100]}...',
            'path': metadata['path'],
            'topico': pathlib.Path(metadata['path']).stem.capitalize().replace('-', ' '),
            'projection_x': metadata['projection_x'],
            'projection_y': metadata['projection_y'],
        }
        for id, chunk, _, metadata in zip(ids, chunks, embeddings, metadatas)
    ])

    # print(df)

    chart = alt.Chart(df).mark_circle(
        size=70,
    ).encode(
        x='projection_x',
        y='projection_y',
        tooltip=['id', 'chunk', 'topico'],
        color=alt.Color('topico', scale=alt.Scale(scheme='tableau20')),
    ).properties(
        title='Proyección de los embeddings',
        width=800,
        height=800,
    ).interactive()

    chart.save('chart.html')

    # query = "¿Qué dice argendata sobre el gasto publico?"
    query = "¿Qué porcentaje del PBI representa el agro?"
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    query_embedding = model.encode([query])

    results = coleccion.query(
        query_embeddings=query_embedding,
        n_results=10,
        include=["metadatas", "documents"],
    )

    ids = results['ids'][0]
    chunks = results['documents'][0]
    metadatas = results['metadatas'][0]

    df = pl.DataFrame([
        {
            'id': id,
            'chunk': chunk,
            #'path': metadata['path'],
            'topico': pathlib.Path(metadata['path']).stem.capitalize().replace('-', ' '),
            'projection_x': metadata['projection_x'],
            'projection_y': metadata['projection_y'],
        }
        for id, chunk, metadata in zip(ids, chunks, metadatas)
    ])

    chart = chart.properties(title='')
    chart += alt.Chart(df).mark_point(
        size=100,
        opacity=1,
        stroke='black',
        color='black',
        shape='circle',
    ).encode(
        x='projection_x',
        y='projection_y',
        tooltip=['id', 'chunk', 'topico'],
        color=alt.Color('topico', scale=alt.Scale(scheme='tableau20')),
    ).properties(
        title=f'Query: {query}',
        width=800,
        height=800,
    )

    chart.save('chart_query.html')



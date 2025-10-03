import pathlib
import pypdf
from tqdm import tqdm

def extraer_textos(path_raw: str, path_processed: str, n_docs: int) -> list[str]:
    path_processed: pathlib.Path = pathlib.Path(path_processed)
    path_processed.mkdir(parents=True, exist_ok=True)
    
    path_raw: pathlib.Path = pathlib.Path(path_raw)
    
    documents = path_raw.glob('**/*.pdf')
    documents = sorted(documents)
    documents = documents[:n_docs]
    documents = [(path, pypdf.PdfReader(path)) for path in documents]

    pbar = tqdm(total=sum(len(document.pages) for _, document in documents), unit='page')

    processed_docs = []
    for path, document in documents:
        processed_filename = path_processed / f"{path.stem}.txt"
        pbar.set_description(f"Processing {path.name}")

        if processed_filename.exists():
            processed_docs.append(processed_filename)
            pbar.update(len(document.pages))
            continue

        text = []
        for page in document.pages:
            text.append(page.extract_text())
            processed_docs.append(processed_filename)
            pbar.update(1)
        
        processed_filename.write_text(''.join(text))
    
    pbar.close()
    return processed_docs

from .download_from_repo import download_from_repo as __get_from_repo

def download(to_local: str = './data/argendata_topicos/processed/'):
    return __get_from_repo(
        from_repo = "argendatafundar/biblioteca/topicos_md", 
        to_local = to_local
    )
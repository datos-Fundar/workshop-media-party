from .download_from_repo import download_from_repo as __get_from_repo

def download(to_local: str = './data/analisis_fmi/raw/'):
    return __get_from_repo(
        from_repo = "datos-Fundar/analisis-fmi/docs", 
        to_local = to_local
    )
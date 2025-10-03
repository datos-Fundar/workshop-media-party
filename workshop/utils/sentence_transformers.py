from typing import TYPE_CHECKING

# Lazy import to avoid long waiting at import-time
if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer
else:
    def SentenceTransformer(*args, quiet_load: bool = True, **kwargs):
        from sentence_transformers import SentenceTransformer
        
        if not quiet_load:
            print(f'Loading SentenceTransformer')
            print(f'Args: {args}')
            print(f'Kwargs: {kwargs}')

        result = SentenceTransformer(*args, **kwargs)
        
        if not quiet_load:
            print(f'Loaded SentenceTransformer!')
        
        return result
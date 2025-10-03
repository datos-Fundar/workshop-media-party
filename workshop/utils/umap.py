from typing import TYPE_CHECKING

# Lazy import to avoid long waiting at import-time
if TYPE_CHECKING:
    from umap import UMAP
else:
    def UMAP(*args, **kwargs):
        from umap import UMAP
        return UMAP(*args, **kwargs)
def is_cuda_available() -> bool:
    from torch import cuda
    return cuda.is_available()
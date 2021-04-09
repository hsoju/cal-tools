import struct
from typing import List, Union


def unpack_chunk(chunk: bytes, fmt: str) -> List[Union[float, int]]:
    container = []
    for value in struct.iter_unpack(fmt, chunk):
        container.append(value[0])
    return container

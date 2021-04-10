import struct
from typing import Callable, Collection, List, Union


def unpack_chunk(chunk: bytes, fmt: str) -> List[Union[float, int]]:
    container = []
    for value in struct.iter_unpack(fmt, chunk):
        container.append(value[0])
    return container


def unpack_values(values: str, fmt: Callable[[str], Union[int, float]]) -> Collection:
    return [fmt(value) for value in values.split()]

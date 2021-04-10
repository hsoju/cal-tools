import struct
from typing import Any, Callable, Collection, Generator, List, Union


def fix_case(tag: str, uppercase: bool) -> str:
    return tag.upper() if uppercase else tag.lower()


def get_cases(uppercase: bool, *tags: str) -> Generator[str, Any, None]:
    return (fix_case(tag, uppercase) for tag in tags)


def unpack_chunk(chunk: bytes, fmt: str) -> List[Union[float, int]]:
    container = []
    for value in struct.iter_unpack(fmt, chunk):
        container.append(value[0])
    return container


def unpack_values(values: str, fmt: Callable[[str], Union[int, float]]) -> Collection:
    return [fmt(value) for value in values.split()]

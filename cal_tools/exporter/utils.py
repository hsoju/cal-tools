from typing import Iterable, Union


def sjoin(values: Iterable[Union[float, int]]) -> str:
    return ' '.join([str(value) for value in values])

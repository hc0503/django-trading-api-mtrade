from typing import Generator, Union

def num_linear_generator(
    initial_num: Union[float, int],
    delta: Union[float, int]
) -> Generator[Union[float, int], None, None]:
    """
    Generates floating point numbers with 'delta' difference from last
    generated number
    """
    next_float = initial_num
    while True:
        yield next_float
        next_float += delta

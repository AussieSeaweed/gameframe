from typing import Any, TypeVar

T = TypeVar('T')


def pretty_print(o: Any, indent: str = '    ', start: str = '', end: str = '\n') -> None:
    """Prints the object on the console prettily.

    :param o: the object
    :param indent: the indentation string
    :param start: the prefix string
    :param end: the suffix string
    :return: None
    """
    if isinstance(o, list):
        print(start + '[')

        for value in o:
            pretty_print(value, indent, start + indent, end=',\n')

        print(start + ']', end=end)
    elif isinstance(o, dict):
        print(start + '{')

        for key, value in o.items():
            print(start + indent + str(key), end=':\n')
            pretty_print(value, indent, start + indent + indent, end=',\n')

        print(start + '}', end=end)
    else:
        print(start + str(o), end=end)


def rotate(collection: list[T], index: int) -> list[T]:
    """Rotates the list by an index.

    :param collection: the list to be rotated
    :param index: the index of rotation
    :return: the rotated list
    """
    return collection[index:] + collection[:index]
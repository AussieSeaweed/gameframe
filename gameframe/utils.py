def pretty_print(o, indent='    ', start='', end='\n'):
    """Prints the object on the console prettily.

    :param o: the object
    :param indent: the indentation string
    :param start: the prefix string
    :param end: the suffix string
    :return: None
    """
    if isinstance(o, dict):
        print(start + '{')

        for key, value in o.items():
            print(start + indent + str(key), end=':\n')
            pretty_print(value, indent, start + indent + indent, end=',\n')

        print(start + '}', end=end)
    elif isinstance(o, list):
        print(start + '[')

        for value in o:
            pretty_print(value, indent, start + indent, end=',\n')

        print(start + ']', end=end)
    else:
        print(start + str(o), end=end)


def rotate(collection, index):
    """Rotates the sequence by an index.

    :param collection: the sequence to be rotated
    :param index: the index of rotation
    :return: the rotated sequence
    """
    return list(collection[index:]) + list(collection[:index])

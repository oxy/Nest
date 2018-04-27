'''
Miscallaneous utils separate from the rest of Nest's core.
'''

from typing import List

def dictwalk(dictionary: dict, tree: List[str], fill: bool = False):
    """Walk down a dictionary tree and return an element.
    Parameters
    ----------
    dictionary: dict
        Dictionary to walk through.
    tree: list
        Sorted tree to walk down.
    fill: bool
        If true, create empty dictionaries
    """

    # Walk the pointer down the tree.
    # Python dictionaries are passed by reference,
    # So iterate over each element in the tree to arrive at
    # the last element.

    item = dictionary
    for k in tree:
        if k not in item:
            if fill:
                item[k] = {}
            else:
                raise ValueError(f'{k} not a valid key.')
        item = item[k]
    return item

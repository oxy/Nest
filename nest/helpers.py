"""
Miscallaneous utils separate from the rest of Nest's core.
"""

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
                raise KeyError(f"{k} not a valid key.")
        item = item[k]
    return item

def smart_truncate(content: str, length: int = 400, suffix: str = "..") -> str:
    """
    Truncates a string to `...` where necessary

    Parameters
    ----------
    content: str
        String to truncate.
    length: int
        Length to truncate to.
    suffix: str = ".."
        String to suffix with.

    Returns
    -------
    str:
        Truncated string.
    """

    if len(content) >= length:
        content = content[:length]
        content = content.rsplit('\n', 1)[0]  # Cut to nearest paragraph.
        content = content.rsplit('.', 1)[0] + "."  # Cut to nearest sentence.
        content += suffix
    return content

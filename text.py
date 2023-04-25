from typing import (
    List,
    Set,
    Sequence,
    Generator,
)
import string

def levenstein_range1(root: Sequence, bases: Sequence=string.ascii_letters) -> List[Sequence]:
    """All sequences within a levenstein distance of 1 from `root`
    Source: https://stackoverflow.com/questions/39858659/what-tool-or-algorithm-should-i-use-to-generate-words-from-a-keyword-which-is-at/

    :param root: root sequence
    :type sequence: Sequence
    :param bases: base set to choose from, defaults to string.ascii_letters
    :type bases: Sequence, optional
    :return: A list of all sequences within a levenstein distance of 1 from `root`
    :rtype: List[Sequence]
    """
    splits = [(root[:i], root[i:]) for i in range(len(root) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    replaces = [L + c + R[1:] for L, R in splits if R for c in bases]
    inserts = [L + c + R for L, R in splits for c in bases]
    return deletes + replaces + inserts


def levenstein_rangex(root: Sequence, bases: Sequence=string.ascii_letters, distance: int=1) -> Set[Sequence]:
    """All sequences within `distance` from `root`
    Source: https://stackoverflow.com/questions/39858659/what-tool-or-algorithm-should-i-use-to-generate-words-from-a-keyword-which-is-at/

    :param root: root sequence
    :type root: Sequence
    :param bases: base set to choose from, defaults to string.ascii_letters
    :type bases: Sequence, optional
    :param distance: distance from root, defaults to 1
    :type distance: int, optional
    :return: A set of all sequences within `distance` from `root`
    :rtype: Set[Sequence]
    """
    if distance == 0:
        return {root}
    elif distance == 1:
        return set(levenstein_range1(root, bases=bases))
    else:
        return set(
            e2 for e1 in levenstein_range1(
                root, bases=bases, edit_distance=distance-1)
            for e2 in levenstein_range1(e1, bases=bases)
        )


def levenstein_generator(root: Sequence, bases: Sequence=string.ascii_letters, distance: int=1) -> Generator[Sequence]:
    """Generate all possible variations of `root` ordered by their levenstein distance, up to `distance`
    Source: https://stackoverflow.com/questions/39858659/what-tool-or-algorithm-should-i-use-to-generate-words-from-a-keyword-which-is-at/

    :param root: root sequence
    :type root: Sequence
    :param bases: base set to choose from, defaults to string.ascii_letters
    :type bases: Sequence, optional
    :param distance: max distance from `root`, defaults to 1
    :type distance: int, optional
    :return: Generator of variations
    :rtype: Generator[Sequence]
    """
    if distance == 0:
        return [root]
    all_editx_minus1 = levenstein_rangex(
        root, bases=bases, distance=distance-1)
    return (
        e2 for e1 in all_editx_minus1
        for e2 in levenstein_range1(e1, bases=bases)
        if e2 not in all_editx_minus1
    )


def sequence_generator(bases: Sequence=string.ascii_letters):
    """Infinitely generate all possible sequences from the bases

    :param bases: base set to choose from, defaults to string.ascii_letters
    :type bases: Sequence, optional
    :yield: Sequence
    """
    cursors = [0]
    while True:
        yield "".join(bases[c] for c in cursors)
        pos = len(cursors)-1
        while pos >= 0 and cursors[pos] == len(bases)-1:
            pos -= 1
        if pos == -1:
            cursors = [0] * (len(cursors)+1)
        else:
            cursors[pos] += 1
            pos += 1
            while pos < len(cursors):
                cursors[pos] = 0
                pos += 1

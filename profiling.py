import sys
import gc

def actualsize(input_obj):
    """
    Source : https://towardsdatascience.com/the-strange-size-of-python-objects-in-memory-ce87bdfbb97f
    """
    memory_size = 0
    ids = set()
    objects = [input_obj]
    while objects:
        new = []
        for obj in objects:
            if id(obj) not in ids:
                ids.add(id(obj))
                memory_size += sys.getsizeof(obj)
                new.append(obj)
        objects = gc.get_referents(*new)
    return memory_size

from collections.abc import Mapping

def deep_merge(d1, d2):
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, Mapping):
            d1[k] = deep_merge(d1[k], v)
        else:
            d1[k] = v
    return d1

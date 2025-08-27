import json, yaml, toml

def detect_format(content):
    loaders = [
        ('json', lambda c: json.loads(c)),
        ('yaml', lambda c: yaml.safe_load(c)),
        ('toml', lambda c: toml.loads(c))
    ]
    for fmt, loader in loaders:
        try:
            return loader(content), fmt
        except Exception:
            continue
    raise ValueError("Unknown or corrupted file format!")

def auto_fix(content):
    fixed = content.strip()
    if fixed and not (fixed.startswith('{') or fixed.startswith('[')):
        fixed = '{' + fixed + '}'
    return fixed

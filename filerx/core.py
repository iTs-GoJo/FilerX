from pathlib import Path
from .parser import detect_format, auto_fix
from .utils import deep_merge
from .watcher import FileWatcher

class FilerX:
    def __init__(self, filepath, watch=False, watch_interval=2):
        self.filepath = Path(filepath)
        self.data = {}
        self.format = None
        self.load()
        if watch:
            self._watcher = FileWatcher(self.filepath, self.load, interval=watch_interval)

    def load(self):
        content = self.filepath.read_text(encoding='utf-8')
        try:
            self.data, self.format = detect_format(content)
        except Exception as e:
            print(f"[WARNING] Load failed: {e}. Trying auto-fix...")
            fixed_content = auto_fix(content)
            self.data, self.format = detect_format(fixed_content)

    def save(self, path=None):
        path = Path(path) if path else self.filepath
        with path.open('w', encoding='utf-8') as f:
            if self.format == 'json':
                import json
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            elif self.format == 'yaml':
                import yaml
                yaml.dump(self.data, f, allow_unicode=True)
            elif self.format == 'toml':
                import toml
                toml.dump(self.data, f)

    def get(self, key_path, default=None):
        keys = key_path.split('.')
        val = self.data
        try:
            for k in keys:
                if isinstance(val, list):
                    k = int(k)
                val = val[k]
            return val
        except (KeyError, IndexError, ValueError, TypeError):
            return default

    def set(self, key_path, value):
        keys = key_path.split('.')
        d = self.data
        for k in keys[:-1]:
            if isinstance(d, list):
                k = int(k)
                while len(d) <= k:
                    d.append({})
                if not isinstance(d[k], dict):
                    d[k] = {}
                d = d[k]
            else:
                if k not in d or not isinstance(d[k], dict):
                    d[k] = {}
                d = d[k]
        last_key = keys[-1]
        if isinstance(d, list):
            last_key = int(last_key)
            while len(d) <= last_key:
                d.append(None)
            d[last_key] = value
        else:
            d[last_key] = value

    def merge(self, other_filepath):
        from .core import FilerX
        other = FilerX(other_filepath)
        self.data = deep_merge(self.data, other.data)

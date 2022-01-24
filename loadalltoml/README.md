# Load TOML config files

This module loads all valid TOML files from a given directory. Config files are stored in a dict with the key being the filename that was loaded.

## Requires

- Python >= 3.7
- tomli >= 1.2.1

---

## Class `LoadAllToml`

### Args

- `config_path`
  - string, relative or absolute path to search for config files.
- `file_pattern`
  - string, `pathlib.glob` pattern to select which files will be loaded. **Default:** `*.toml`

### Properties

- `__len__`
  - Returns the number of configs currently loaded
- `configs`
  - Returns a list of strings. The values are the keys of the configs loaded (filenames)

### Methods

- `load()`
  - Loads valid TOML files from the set `config_path` that match the `file_pattern`.
- `get(<config_name>)`
  - Uses `config_name` as a key and returns the matching value in the loaded configs. The return value, if found, will be a dictionary otherwise it will be `None`

---

## Example

### `example.py`

```py
"""
Example use. Turns debug logging on for example output.
"""
import logging

from load_all_toml import LoadAllToml

logging.basicConfig(level="DEBUG")

# Assumes we are running from the repo structure in `/loadalltoml`
config_loader = LoadAllToml("tests/configs")

config_loader.load()

print(config_loader.configs, end="\n\n")

print(config_loader.get("config01.toml"))
```

### Output

```py
$ python example.py
DEBUG:load_all_toml:Loaded: `tests/configs/config03.toml`
DEBUG:load_all_toml:Loaded: `tests/configs/config01.toml`
DEBUG:load_all_toml:Loaded: `tests/configs/config02.toml`
INFO:load_all_toml:Finished loading 3 config files
['config03.toml', 'config01.toml', 'config02.toml']

{'config': {'string_value': 'test1', 'list_value1': ['this', 'is', 'a', 'list'], 'list_value2': ['Here', 'is', 'another', 'list']}}
```

---

## Tests

To run tests:

`python -m pytest`

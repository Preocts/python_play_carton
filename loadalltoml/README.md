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

## Tests

To run tests:

`python -m pytest`

import logging
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import tomli


class LoadAllToml:
    def __init__(self, config_path: str, file_pattern: str = "*.toml") -> None:
        """Provide the absolute or relative path of `.toml` files"""
        self.log = logging.getLogger(__name__)
        self.config_path = config_path
        self.file_pattern = file_pattern
        self._loaded_configs: Dict[str, Dict[str, Any]] = {}

    def __len__(self) -> int:
        """Return the number of loaded config files"""
        return len(self._loaded_configs)

    @property
    def configs(self) -> List[str]:
        """Returns a list of available configs"""
        return list(self._loaded_configs.keys())

    def get(self, config_name: str) -> Optional[Dict[str, Any]]:
        """Returns specific config if found"""
        if config_name in self._loaded_configs:
            return self._loaded_configs[config_name].copy()
        return None

    def load(self) -> None:
        """Loads all valid config files in `config_path` matching `file_pattern`"""
        # Always reset the cache on load to ensure clean loading, no side-effects
        self._loaded_configs = {}
        for filename in Path(self.config_path).glob(self.file_pattern):
            try:
                with open(filename, "rb") as infile:
                    loaded = tomli.load(infile)
            except tomli.TOMLDecodeError:
                self.log.error("'%s' - invalid toml format", filename)
                continue
            self._loaded_configs[filename.name] = loaded
            self.log.debug("Loaded: `%s`", filename)
        self.log.info("Finished loading %s config files", len(self._loaded_configs))

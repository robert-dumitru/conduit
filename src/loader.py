import os
import tomllib

from pydantic import BaseModel


class SourceConfig(BaseModel):
    entry_file: str = "entry.sh"


class Loader:
    """Loads configs from a directory for conduit sources"""

    def __init__(self, pathname: str):
        self.pathname = pathname
        self.path = os.path.dirname(self.pathname)
        self.configs = []

    def load_configs(self):
        """Loads configs from the specified directory"""
        self._validate_configs()
        return self.configs

    def _validate_configs(self):
        """Validates each source has a valid entry file"""
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File not found: {self.path}")

        for item in os.listdir(self.path):
            folder_path = os.path.join(self.path, item)
            if not os.path.isdir(folder_path):
                continue

            self.folders.append(item)
            config = self._validate_config_folder(folder_path)
            self.configs.append(config)

    @staticmethod
    def _validate_config_folder(folder_path: str):
        """Validates a folder has a valid entry file"""
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        config = None
        toml_path = os.path.join(folder_path, "config.toml")

        if os.path.exists(toml_path):
            config = tomllib.load(open(toml_path, "rb"))
            config = SourceConfig(**config)
        else:
            config = SourceConfig()

        if not os.path.exists(os.path.join(folder_path, config.entry_file)):
            raise FileNotFoundError(
                f"Entry file '{config.entry_file}' not found in folder: {folder_path}"
            )

        return config

import os

from pydantic import BaseModel
from subprocess import Popen, PIPE


class SourceConfig(BaseModel):
    folder_path: str
    entry_file: str = "entry.sh"
    dependencies: list[str] = []

    def entry_cmd(self):
        return os.path.join(self.folder_path, self.entry_file)


class Source:
    """Represents a source in the conduit"""

    def __repr__(self):
        return f"Source(config={self.config.model_dump_json()})"

    def __init__(self, config: SourceConfig):
        self.config = config
        self.has_run = False

    def run(self) -> str:
        """Runs the source"""
        if self.has_run:
            return

        self.has_run = True
        process = Popen(self.config.entry_cmd, stdout=PIPE, text=True)
        output, _ = process.communicate()
        return output

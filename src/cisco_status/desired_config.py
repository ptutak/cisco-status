from pydantic import BaseModel
import os

class DesiredHSRPConfig(BaseModel):
    interface: str
    group: int
    status: str

    @classmethod
    def parse_file(self, filename: os.PathLike[str]) -> "DesiredHSRPConfig":
        with open(filename) as file:
            content = file.read()
            return self.model_validate_json(content)

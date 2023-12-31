from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    data_path: Path = Path("data/output")
    upload_path: Path = Path("data/upload")
    temp_path: Path = Path("data/temp")

    read_chuck: int = 10240
    max_size: int = 300 * 1024 ** 2

    call_cd: float = 10


config = Config()

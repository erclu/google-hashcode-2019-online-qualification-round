from pathlib import Path
from typing import List


def read_photos_file(filename: Path) -> List[str]:
    lines = filename.read_text().split("\n")
    return lines[1:-1]

from pathlib import Path
from typing import List

from . import model


def photos_from_file(filename: Path) -> List[model.Photo]:
    content = filename.read_text()
    # skip first and last line in file
    photos_lines: List[str] = content.split("\n")[1:-1]

    return [model.Photo.from_str(pid, x) for pid, x in enumerate(photos_lines)]


def write_output_file(filename: Path, slideshow: model.Slideshow) -> None:
    filename.write_text(slideshow.to_string(), encoding="UTF-8")

from pathlib import Path
from random import randrange
from typing import List

from tqdm import tqdm

from . import model
from .utils import photos_from_file, write_output_file


def _solve(photos: List[model.Photo]) -> model.Slideshow:

    raise NotImplementedError()


def do_all():
    _parent_folder: Path = Path(__file__).resolve().parents[1]

    input_folder: Path = _parent_folder.joinpath("in")
    output_folder: Path = _parent_folder.joinpath("out")

    input_files = input_folder.glob("input*")

    file: Path
    for file in input_files:
        output_file = output_folder/file.name.replace("input", "output")

        photos: List[model.Photo] = photos_from_file(file)

        slideshow: model.Slideshow = _solve(photos)

        write_output_file(output_file, slideshow)


def do_one(file: str):

    input_file: Path = Path(file).resolve()

    photos: List[model.Photo] = photos_from_file(input_file)

    slideshow: model.Slideshow = _solve(photos)
    # write_output_file(output_file, slideshow)

    print(slideshow.score())

import random
from pathlib import Path
from typing import List

from tqdm import tqdm

from . import model


#TODO refactor _solve to solve
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

        photos: List[model.Photo] = model.Photo.from_file(file)

        slideshow: model.Slideshow = _solve(photos)

        slideshow.save(output_file)


def do_one(file: str):
    input_file: Path = Path(file).resolve()

    photos: List[model.Photo] = model.Photo.from_file(input_file)
    slideshow: model.Slideshow = _solve(photos)
    print(slideshow.score())

    output_file: Path = Path.cwd().joinpath(f"out-{slideshow.score()}.txt")

    slideshow.save(output_file)

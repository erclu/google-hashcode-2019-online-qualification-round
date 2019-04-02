# pylint: disable=redefined-outer-name
from pathlib import Path
from typing import List

import pytest

from solver import model
from solver.solve import _solve


def test_solve():
    example_file: Path = Path(__file__).resolve().parents[1].joinpath(
      "in", "a_example.txt"
    )
    assert example_file.exists()

    photos: List[model.Photo] = model.Photo.from_file(example_file)

    slideshow: model.Slideshow = _solve(photos)

    # assert (
    #   slideshow.to_string() == "3\n0\n3\n1 2\n" or
    #   slideshow.to_string() == "3\n0\n3\n2 1\n" or
    #   slideshow.to_string() == "3\n1 2\n3\n0\n" or
    #   slideshow.to_string() == "3\n2 1\n3\n0\n"
    # )
    assert slideshow.score() == 2


# TODO test on input2 (smaller one)
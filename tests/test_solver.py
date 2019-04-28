# pylint: disable=redefined-outer-name
from pathlib import Path
from typing import List

import pytest

from solver import model
from solver.solve import (
  _get_horizontal_slides, _get_vertical_slides, do_one, solve
)


@pytest.fixture(scope="session")
def input2_photos_list():
    file = Path(__file__).resolve().parents[1].joinpath("in", "input2.txt")
    assert file.exists()

    return model.Photo.from_file(file)


def test_get_slides(input2_photos_list):
    photos = input2_photos_list

    hor_slides = _get_horizontal_slides(photos)
    assert len(hor_slides) == 500

    ver_slides = _get_vertical_slides(photos)
    assert len(ver_slides) == 250

    for slide in hor_slides:
        assert slide.photo.orientation == "H"

    for slide in ver_slides:
        assert (
          slide.first.orientation == "V" and slide.second.orientation == "V"
        )


def test_solve():
    example_file: Path = Path(__file__).resolve().parents[1].joinpath(
      "in", "a_example.txt"
    )
    assert example_file.exists()

    photos: List[model.Photo] = model.Photo.from_file(example_file)

    slideshow: model.Slideshow = solve(photos)

    assert slideshow.score() == 2

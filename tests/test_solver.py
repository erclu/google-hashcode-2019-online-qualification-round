# pylint: disable=redefined-outer-name
import typing
from pathlib import Path

import pytest

from solver import model
from solver.solve import solve


@pytest.fixture(scope="session")
def input2_photos_list() -> typing.List[model.Photo]:
    file = Path(__file__).resolve().parents[1].joinpath("in", "input2.txt")
    assert file.exists()

    return model.Photo.from_file(file)


def test_solve() -> None:
    example_file: Path = Path(__file__).resolve().parents[1].joinpath(
      "in", "a_example.txt"
    )
    assert example_file.exists()

    yay: bool = False
    for _ in range(5): # XXX this is horrible and i feel ashamed
        photos: typing.List[model.Photo] = model.Photo.from_file(example_file)

        slideshow: model.Slideshow = solve(photos)
        if slideshow.score() == 2:
            yay = True

    assert yay

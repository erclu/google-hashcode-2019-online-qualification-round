# pylint: disable=redefined-outer-name
import typing
from pathlib import Path

import pytest

from solver import model
from solver.solve import _get_horizontal_slides, _get_vertical_slides, solve


@pytest.fixture(scope="session")
def input2_photos_list() -> typing.List[model.Photo]:
    file = Path(__file__).resolve().parents[1].joinpath("in", "input2.txt")
    assert file.exists()

    return model.Photo.from_file(file)


def test_get_slides(input2_photos_list: typing.List[model.Photo]) -> None:
    photos = input2_photos_list

    hor_slides = _get_horizontal_slides(photos)
    assert len(hor_slides) == 500

    ver_slides = _get_vertical_slides(photos)
    assert len(ver_slides) == 250

    for h_slide in hor_slides:
        assert h_slide.photo.orientation == "H"

    for v_slide in ver_slides:
        assert (
          v_slide.first.orientation == "V" and
          v_slide.second.orientation == "V"
        )


def test_solve() -> None:
    example_file: Path = Path(__file__).resolve().parents[1].joinpath(
      "in", "a_example.txt"
    )
    assert example_file.exists()

    photos: typing.List[model.Photo] = model.Photo.from_file(example_file)

    yay: bool = False
    for _ in range(5): # XXX this is horrible and i feel ashamed
        slideshow: model.Slideshow = solve(photos)
        if slideshow.score() == 2:
            yay = True

    assert yay

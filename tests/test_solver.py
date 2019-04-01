from pathlib import Path
from typing import List

import pytest

from solver import model
from solver.solve import _solve
from solver.utils import photos_from_file


@pytest.mark.skip(reason="not implemented yet")
def test_solve():
    example_file: Path = Path(__file__
                              ).resolve().parents[1]/"in"/"a_example.txt"
    assert example_file.exists()

    photos: List[model.Photo] = photos_from_file(example_file)

    slideshow: model.Slideshow = _solve(photos)

    assert (
      slideshow.to_string() == "3\n0\n3\n1 2"
      or slideshow.to_string() == "3\n1 2\n3\n0"
    )
    assert slideshow.score() == 2

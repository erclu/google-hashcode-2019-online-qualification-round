from pathlib import Path
from typing import List

import pytest

from solver import model
from solver.solve import _solve
from solver.utils import photos_from_file, write_output_file


def test_solve():
    example_file: Path = Path(__file__
                              ).resolve().parents[1]/"in"/"a_example.txt"
    assert example_file.exists()

    photos: List[model.Photo] = photos_from_file(example_file)

    with pytest.raises(NotImplementedError) as err:
        slideshow: model.Slideshow = _solve(photos)

    return

    assert (
      slideshow.to_string() == "3\n0\n3\n1 2"
      or slideshow.to_string() == "3\n1 2\n3\n0"
    )
    assert slideshow.score() == 2

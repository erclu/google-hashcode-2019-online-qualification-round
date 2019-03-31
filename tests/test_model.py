from pathlib import Path

import solver.utils
from solver.model import Photo


def test_example_file():
    example_file: Path = Path(__file__
                              ).resolve().parents[1]/"in"/"a_example.txt"
    assert example_file.exists()

    lines = solver.utils.read_photos_file(example_file)
    photos = [Photo.from_str(pid, x) for pid, x in enumerate(lines)]

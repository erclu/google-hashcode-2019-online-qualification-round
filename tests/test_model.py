# pylint: disable=redefined-outer-name
from itertools import permutations
from pathlib import Path

import pytest

from solver import model


@pytest.fixture(scope="session")
def example_photos():
    example_file: Path = Path(__file__).resolve().parents[1].joinpath(
      "in", "a_example.txt"
    )
    assert example_file.exists()

    return model.Photo.from_file(example_file)


def test_example_file(example_photos):

    hor_slide = model.HorizontalSlide(example_photos[0])
    another_hor_slide = model.HorizontalSlide(example_photos[3])
    vert_slide = model.VerticalSlide(example_photos[1], example_photos[2])

    assert all(tag in hor_slide.tags for tag in ["cat", "beach", "sun"])
    assert another_hor_slide.photo.orientation == "H"
    assert vert_slide.tags == {"selfie", "smile", "garden"}

    slides_list = [hor_slide, another_hor_slide, vert_slide]

    results = [2, 1, 1, 1, 1, 2]

    for perm, result in zip(permutations(slides_list), results):
        slideshow = model.Slideshow.from_list(perm)
        assert slideshow.score() == result


def test_write(example_photos, tmp_path):
    slides_list = [
      model.HorizontalSlide(example_photos[0]),
      model.HorizontalSlide(example_photos[3]),
      model.VerticalSlide(example_photos[1], example_photos[2])
    ]
    slideshow = model.Slideshow.from_list(slides_list)

    example_out_file: Path = tmp_path.joinpath("output_of_example.txt")

    slideshow.save(example_out_file)


def test_slideshow_score():
    scores_iterator = iter([21081, 1416, 412436, 361153])

    _parent_folder = Path(__file__).resolve().parents[1]

    input_files: Path = _parent_folder.joinpath("in").glob("input*txt")
    solution_files: Path = _parent_folder.joinpath("submitted_outputs"
                                                   ).glob("output*txt")

    for input_file, solution in zip(input_files, solution_files):

        photos = model.Photo.from_file(input_file)

        sol_indexes = solution.read_text().split("\n")[1:-1]

        slideshow = model.Slideshow()

        for str_index in sol_indexes:
            if " " not in str_index:
                index = int(str_index)
                photo: model.Photo = photos[index]
                assert photo.photo_id == index
                slide: model.HorizontalSlide = model.HorizontalSlide(photo)
            else:
                i, j = [int(x) for x in str_index.split(" ")]
                slide: model.VerticalSlide = model.VerticalSlide(
                  photos[i], photos[j]
                )
                assert slide.first.photo_id == i and slide.second.photo_id == j

            slideshow.append(slide)

        assert slideshow.score() == next(scores_iterator)


#TODO add test to check output file validity
@pytest.mark.skip(reason="not implemented yet")
def test_output_file():
    assert 0

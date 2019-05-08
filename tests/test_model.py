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


def test_equality():
    args = [1, "H", {"a", "b", "c"}]

    h_photo_1 = model.Photo(*args)
    h_photo_1_bis = model.Photo(*args)

    h_photo_2 = model.Photo(2, "H", {"a"})

    h_slide_1 = model.HorizontalSlide(h_photo_1)
    h_slide_1_bis = model.HorizontalSlide(h_photo_1_bis)

    h_slide_2 = model.HorizontalSlide(h_photo_2)

    assert h_slide_1 == h_slide_1_bis
    assert h_slide_1 != h_slide_2

    class Dummy: # pylint: disable=too-few-public-methods

        def __init__(self):
            self.dummy_var = "hello"

    dummy_obj = Dummy()

    assert h_slide_1 != dummy_obj

    args2_a = [1, "V", {"a", "b"}]
    args2_b = [2, "V", {"b", "c"}]
    args2_c = [3, "V", {"a", "b", "d"}]

    v_photo_a = model.Photo(*args2_a)
    v_photo_b = model.Photo(*args2_b)

    v_photo_c = model.Photo(*args2_c)

    v_slide_1 = model.VerticalSlide(v_photo_a, v_photo_b)
    v_slide_2 = model.VerticalSlide(v_photo_a, v_photo_b)
    v_slide_3 = model.VerticalSlide(v_photo_a, v_photo_c)

    assert v_slide_1 == v_slide_2
    assert v_slide_1 != v_slide_3


def test_slideshow_score():
    """uses submitted files to check that score function works correctly
    """
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
                assert int(photo.photo_id) == index
                slide: model.HorizontalSlide = model.HorizontalSlide(photo)
            else:
                i, j = [int(x) for x in str_index.split(" ")]
                slide: model.VerticalSlide = model.VerticalSlide(
                  photos[i], photos[j]
                )
                assert int(slide.first.photo_id
                           ) == i and int(slide.second.photo_id) == j

            slideshow.append(slide)

        assert slideshow.score() == next(scores_iterator)

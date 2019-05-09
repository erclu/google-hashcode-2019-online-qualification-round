# pylint: disable=redefined-outer-name
import typing
from itertools import permutations
from pathlib import Path

import pytest

from solver import model


@pytest.fixture(scope="session")
def example_photos() -> typing.List[model.Photo]:
    example_file: Path = Path(__file__).resolve().parents[1].joinpath(
      "in", "a_example.txt"
    )
    assert example_file.exists()

    return model.Photo.from_file(example_file)


def test_example_file(example_photos: typing.List[model.Photo]) -> None:

    hor_slide = model.HorizontalSlide(example_photos[0])
    another_hor_slide = model.HorizontalSlide(example_photos[3])
    vert_slide = model.VerticalSlide(example_photos[1], example_photos[2])

    assert all(tag in hor_slide.tags for tag in ["cat", "beach", "sun"])
    assert another_hor_slide.photo.orientation == "H"
    assert vert_slide.tags == {"selfie", "smile", "garden"}

    slides_list = [hor_slide, another_hor_slide, vert_slide]

    results = [2, 1, 1, 1, 1, 2]

    for perm, result in zip(permutations(slides_list), results):
        slideshow = model.Slideshow.from_list(list(perm))
        assert slideshow.score() == result


def test_write(
  example_photos: typing.List[model.Photo], tmp_path: Path
) -> None:
    slides_list = [
      model.HorizontalSlide(example_photos[0]),
      model.HorizontalSlide(example_photos[3]),
      model.VerticalSlide(example_photos[1], example_photos[2])
    ]
    slideshow = model.Slideshow.from_list(slides_list)

    example_out_file: Path = tmp_path.joinpath("output_of_example.txt")

    slideshow.save(example_out_file)


def test_equality() -> None:
    Photo_init_args = typing.Tuple[int, str, typing.Set[str]]
    args: Photo_init_args = (1, "H", {"a", "b", "c"})

    h_photo_1 = model.Photo(*args)
    h_photo_1_bis = model.Photo(*args)

    h_photo_2 = model.Photo(2, "H", {"a"})

    h_slide_1 = model.HorizontalSlide(h_photo_1)

    assert h_slide_1 == model.HorizontalSlide(h_photo_1_bis)
    assert h_slide_1 != model.HorizontalSlide(h_photo_2)

    class Dummy: # pylint: disable=too-few-public-methods

        def __init__(self) -> None:
            self.dummy_var = "hello"

    dummy_obj = Dummy()

    assert h_slide_1 != dummy_obj

    args2_a: Photo_init_args = (1, "V", {"a", "b"})
    args2_b: Photo_init_args = (2, "V", {"b", "c"})
    args2_c: Photo_init_args = (3, "V", {"a", "b", "d"})

    v_photo_a = model.Photo(*args2_a)
    v_photo_b = model.Photo(*args2_b)
    v_photo_c = model.Photo(*args2_c)

    v_slide_1 = model.VerticalSlide(v_photo_a, v_photo_b)

    assert v_slide_1 == model.VerticalSlide(v_photo_a, v_photo_b)
    assert v_slide_1 != model.VerticalSlide(v_photo_a, v_photo_c)


def test_slotted() -> None:
    h_photo = model.Photo(1, "H", {"a", "b", "c"})
    v_photo_1 = model.Photo(1, "V", {"a", "b"})
    v_photo_2 = model.Photo(2, "V", {"b", "c"})

    my_classes = (
      h_photo,
      model.HorizontalSlide(h_photo),
      model.VerticalSlide(v_photo_1, v_photo_2),
      model.Slideshow(),
    )

    for my_class in my_classes:
        assert my_class.__slots__
        with pytest.raises(AttributeError):
            assert my_class.__dict__


@pytest.mark.slow
def test_slideshow_score() -> None:
    """uses submitted files to check that score function works correctly
    """
    scores_iterator = iter([21081, 1416, 412436, 361153])

    _parent_folder = Path(__file__).resolve().parents[1]

    input_files = _parent_folder.joinpath("in").glob("input*txt")
    solution_files = _parent_folder.joinpath("submitted_outputs"
                                             ).glob("output*txt")

    input_file: Path
    solution_file: Path
    for input_file, solution_file in zip(input_files, solution_files):

        photos = model.Photo.from_file(input_file)

        sol_indexes = solution_file.read_text().split("\n")[1:-1]

        slideshow = model.Slideshow()

        for str_index in sol_indexes:
            slide: typing.Union[model.HorizontalSlide, model.VerticalSlide]
            if " " not in str_index:
                index = int(str_index)
                photo: model.Photo = photos[index]
                assert int(photo.photo_id) == index
                slide = model.HorizontalSlide(photo)
            else:
                i, j = [int(x) for x in str_index.split(" ")]
                slide = model.VerticalSlide(photos[i], photos[j])
                assert int(slide.first.photo_id
                           ) == i and int(slide.second.photo_id) == j

            slideshow.append(slide)

        assert slideshow.score() == next(scores_iterator)

from itertools import permutations
from pathlib import Path

from solver import model
from solver.utils import photos_from_file, write_output_file


def test_example_file():
    example_file: Path = Path(__file__
                              ).resolve().parents[1]/"in"/"a_example.txt"
    assert example_file.exists()

    photos = photos_from_file(example_file)

    hor_slide = model.HorizontalSlide(photos[0])
    another_hor_slide = model.HorizontalSlide(photos[3])
    vert_slide = model.VerticalSlide(photos[1], photos[2])

    assert all(tag in hor_slide.tags for tag in ["cat", "beach", "sun"])
    assert another_hor_slide.photo.orientation == "H"
    assert vert_slide.tags == {"selfie", "smile", "garden"}

    slides_list = [hor_slide, another_hor_slide, vert_slide]

    results = [2, 1, 1, 1, 1, 2]

    for perm, result in zip(permutations(slides_list), results):
        slideshow = model.Slideshow.from_list(perm)
        assert slideshow.score() == result


def test_write():
    example_file: Path = Path(__file__
                              ).resolve().parents[1]/"in"/"a_example.txt"
    assert example_file.exists()

    photos = photos_from_file(example_file)

    slides_list = [
      model.HorizontalSlide(photos[0]),
      model.HorizontalSlide(photos[3]),
      model.VerticalSlide(photos[1], photos[2])
    ]
    slideshow = model.Slideshow.from_list(slides_list)

    example_out_file: Path = Path(__file__).resolve(
    ).parents[1]/"out"/"output_of_example.txt"

    write_output_file(example_out_file, slideshow.to_string())

    #TODO improve this test (fixtures?)


def test_slideshow_score():
    scores = [21081, 1416, 412436, 361153]
    _parent_folder = Path(__file__).resolve().parents[1]

    for x in range(1, 5):
        input_file: Path = _parent_folder.joinpath("in", f"input{x}.txt")
        solution: Path = _parent_folder.joinpath(
          "out_submitted", f"output{x}.txt"
        )
        assert input_file.exists() and solution.exists()

        photos = photos_from_file(input_file)

        sol_indexes = solution.read_text().split("\n")[1:-1]

        slideshow = model.Slideshow()

        for str_index in sol_indexes:
            if " " not in str_index:
                index = int(str_index)
                photo: model.Photo = photos[index]
                assert photo.photo_id == index
                slide: model.HorizontalSlide = model.HorizontalSlide(photo)
            else:
                split_str_index = str_index.split(" ")
                i, j = int(split_str_index[0]), int(split_str_index[1])
                first_photo: model.Photo = photos[i]
                second_photo: model.Photo = photos[j]
                assert first_photo.photo_id == i and second_photo.photo_id == j
                slide: model.VerticalSlide = model.VerticalSlide(
                  first_photo, second_photo
                )

            slideshow.append(slide)

        assert slideshow.score() == scores[x - 1]

    # assert False

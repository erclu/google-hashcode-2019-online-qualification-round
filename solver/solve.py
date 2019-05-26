import random
import typing
from itertools import islice
from pathlib import Path

from tqdm import tqdm

from . import model

# max points with:
# WINDOW_SIZE = 10000
# VERTICAL_WINDOW_SIZE = 10000
#
# input1 109359
# input2 1749
# input3 387601 XXX still bad
# input4 495386
WINDOW_SIZE = 2000
VERTICAL_WINDOW_SIZE = 2000


def solve(photos: typing.List[model.Photo]) -> model.Slideshow:
    slideshow: model.Slideshow = model.Slideshow()

    current_slide: model.Slide

    random.shuffle(photos)
    # sorted(photos, key=lambda photo: len(photo.tags))
    first_photo: model.Photo = photos.pop(0)

    if first_photo.orientation == "H":
        current_slide = model.HorizontalSlide(first_photo)
    else:
        second_photo = next(filter(lambda x: x.orientation == "V", photos))
        photos.remove(second_photo)

        current_slide = model.VerticalSlide(first_photo, second_photo)

    slideshow.append(current_slide)

    with tqdm(total=len(photos), ascii=True) as pbar:
        while photos:
            sliding_window = islice(photos, WINDOW_SIZE)
            best_photo: model.Photo = max(
              sliding_window,
              key=lambda ph: model.score_tags(current_slide.tags, ph.tags)
            )
            photos.remove(best_photo)

            best_slide: model.Slide
            if best_photo.orientation == "H":
                best_slide = model.HorizontalSlide(best_photo)
            else:
                vertical_photos_window = islice(
                  filter(lambda x: x.orientation == "V", photos),
                  VERTICAL_WINDOW_SIZE
                )
                other_best_photo: model.Photo = max(
                  vertical_photos_window,
                  key=lambda ph: model.score_tags(
                    current_slide.tags, ph.tags.union(best_photo.tags)
                  )
                )
                photos.remove(other_best_photo)

                pbar.update()

                best_slide = model.VerticalSlide(best_photo, other_best_photo)

            current_slide = best_slide
            slideshow.append(best_slide)

            pbar.set_postfix_str(s="score: " + str(slideshow.score()))
            pbar.update()

    return slideshow


def do_one(file: str) -> None:
    input_file: Path = Path(file).resolve()

    photos: typing.List[model.Photo] = model.Photo.from_file(input_file)
    slideshow: model.Slideshow = solve(photos)
    print(slideshow.score())

    input_name: str = input_file.name.replace(".txt", "")
    output_file: Path = Path.cwd().joinpath(
      "out_do_one",
      "out-from_{}-score_{}.txt".format(input_name, slideshow.score())
    )

    slideshow.save(output_file)


def profile_me() -> None:
    import line_profiler
    lineprof = line_profiler.LineProfiler()
    wrapped_solve = lineprof(solve)

    input2 = Path(__file__).resolve().parents[1].joinpath("in", "input2.txt")
    photos: typing.List[model.Photo] = model.Photo.from_file(input2)
    slideshow: model.Slideshow = wrapped_solve(photos)

    print(slideshow.score())

    lineprof.print_stats()

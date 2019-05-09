import random
import typing
from itertools import islice
from pathlib import Path

from tqdm import tqdm

from . import model


def _get_horizontal_slides(photos: typing.List[model.Photo]
                           ) -> typing.List[model.HorizontalSlide]:
    return [
      model.HorizontalSlide(ph) for ph in photos if ph.orientation == "H"
    ]


def _get_vertical_slides(photos: typing.List[model.Photo]
                         ) -> typing.List[model.VerticalSlide]:
    vertical_photos = list(filter(lambda x: x.orientation == "V", photos))
    sorted(vertical_photos, key=lambda ph: len(ph.tags))

    vertical_slides: typing.List[model.VerticalSlide] = []

    # TODO refactor with itertools!
    while vertical_photos:
        current = vertical_photos.pop(0)

        if not vertical_photos:
            break # handle case with odd number of vertical photos

        other = vertical_photos.pop()
        # other = random.choice(vertical_photos)
        # vertical_photos.remove(other)

        vertical_slides.append(model.VerticalSlide(current, other))

    return vertical_slides


def solve(photos: typing.List[model.Photo]) -> model.Slideshow:

    slides: typing.List[model.Slide] = (
      _get_horizontal_slides(photos) + _get_vertical_slides(photos)
    )
    print("------------ made slides from photos ------------")

    slideshow: model.Slideshow = model.Slideshow()

    random.shuffle(slides)
    # sorted(slides, key=lambda slide: len(slide.tags), reverse=True)
    # sorted(slides, key=lambda slide: len(slide.tags))
    current_slide: model.Slide = slides.pop(0)

    slideshow.append(current_slide)

    # less than 500 gets awful scores
    window_size = 2000
    with tqdm(total=len(slides), ascii=True) as pbar:
        #TODO refactor with itertools
        while slides:
            sliding_window = islice(slides, window_size)

            best_slide: model.Slide = max(
              sliding_window,
              key=lambda sl: model.score_tags(current_slide.tags, sl.tags)
            )

            slides.remove(best_slide)
            slideshow.append(best_slide)

            current_slide = best_slide
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

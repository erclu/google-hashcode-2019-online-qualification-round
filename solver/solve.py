import random
import typing
from pathlib import Path

from tqdm import tqdm

from . import model


def _get_horizontal_slides(photos: typing.List[model.Photo]
                           ) -> typing.List[model.HorizontalSlide]:
    return [
      model.HorizontalSlide(ph) for ph in photos if ph.orientation == "H"
    ]


def _match_vertical_photos(
  photo: model.Photo, matches: typing.List[model.Photo]
) -> model.Photo:
    """contains the logic for matching vertical photos into a slide"""
    return matches[-1]


def _get_vertical_slides(photos: typing.List[model.Photo]
                         ) -> typing.List[model.VerticalSlide]:
    vertical_photos = list(filter(lambda x: x.orientation == "V", photos))
    sorted(vertical_photos, key=lambda ph: len(ph.tags))

    vertical_slides: typing.List[model.VerticalSlide] = []

    # TODO refactor with itertools!
    while vertical_photos:
        current: model.Photo = vertical_photos.pop(0)

        if not vertical_photos:
            break # handle case with odd number of vertical photos

        other: model.Photo = _match_vertical_photos(current, vertical_photos)

        vertical_photos.remove(other)

        vertical_slides.append(model.VerticalSlide(current, other))

    return vertical_slides


def solve(photos: typing.List[model.Photo]) -> model.Slideshow:

    slides: typing.List[model.Slide] = _get_horizontal_slides(photos)
    slides.extend(_get_vertical_slides(photos))
    print("------------ made slides from photos ------------")

    slideshow: model.Slideshow = model.Slideshow()

    random.shuffle(slides)
    sorted(slides, key=lambda sl: len(sl.tags))
    current_slide: model.Slide = slides.pop(0)

    slideshow.append(current_slide)

    # XXX less than 500 gets bad scores
    window_size = 5000
    with tqdm(total=len(slides)) as pbar:
        #TODO refactor with itertools
        while slides:
            max_score: int = -1
            best_slide: model.Slide = None

            sliding_window = slides[:window_size]

            for next_slide in sliding_window:
                new_score = model.score_tags(
                  current_slide.tags, next_slide.tags
                )
                if new_score > max_score:
                    max_score = new_score
                    best_slide = next_slide

            # XXX this is O(n), but the time spent on this line is low...
            slides.remove(best_slide)
            slideshow.append(best_slide)

            current_slide = best_slide
            pbar.set_postfix_str(s="score: " + str(slideshow.score()))
            pbar.update()

    return slideshow


def do_one(file: str):
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


def profile_me():
    import line_profiler
    lineprof = line_profiler.LineProfiler()
    wrapped_solve = lineprof(solve)

    input2 = Path(__file__).resolve().parents[1].joinpath("in", "input2.txt")
    photos: typing.List[model.Photo] = model.Photo.from_file(input2)
    slideshow: model.Slideshow = wrapped_solve(photos)

    print(slideshow.score())

    lineprof.print_stats()

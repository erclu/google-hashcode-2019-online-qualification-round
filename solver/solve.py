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


def _get_vertical_slides(photos: typing.List[model.Photo]
                         ) -> typing.List[model.VerticalSlide]:
    vertical_photos = list(filter(lambda x: x.orientation == "V", photos))

    vertical_slides: typing.List[model.VerticalSlide] = []

    def match_vertical_photos(
      photo: model.Photo, matches: typing.List[model.Photo]
    ) -> model.Photo:
        """contains the logic for matching vertical photos into a slide"""
        return random.sample(matches, 1)[0]

        # max_score: int = -1
        # best_photo: model.Slide = None

        # window_size = 500
        # sliding_window = random.sample(matches, min(window_size, len(matches)))
        # for other_photo in sliding_window:
        #     new_score = model.score_tags(photo.tags, other_photo.tags)
        #     if new_score > max_score:
        #         max_score = new_score
        #         best_photo = other_photo

        # return best_photo

    # TODO refactor with itertools!
    while vertical_photos:
        current: model.Photo = vertical_photos.pop(0)

        if not vertical_photos:
            break # handle case with odd number of vertical photos

        other: model.Photo = match_vertical_photos(current, vertical_photos)

        vertical_photos.remove(other)

        vertical_slides.append(model.VerticalSlide(current, other))

    return vertical_slides


def solve(photos: typing.List[model.Photo]) -> model.Slideshow:

    slides: typing.List[model.Slide] = _get_horizontal_slides(photos)
    slides.extend(_get_vertical_slides(photos))
    print("------------ made slides from photos ------------")

    slideshow: model.Slideshow = model.Slideshow()

    random.shuffle(slides)
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


def do_all():
    _parent_folder: Path = Path(__file__).resolve().parents[1]

    input_folder: Path = _parent_folder.joinpath("in")
    output_folder: Path = _parent_folder.joinpath("out")

    input_files = input_folder.glob("input*")

    input_file: Path
    for input_file in input_files:
        photos: typing.List[model.Photo] = model.Photo.from_file(input_file)

        slideshow: model.Slideshow = solve(photos)

        output_file: Path = output_folder.joinpath(
          input_file.name.replace("input", "output").replace(
            ".txt", "{}.txt".format(slideshow.score())
          )
        )
        slideshow.save(output_file)


def do_one(file: str):
    input_file: Path = Path(file).resolve()

    photos: typing.List[model.Photo] = model.Photo.from_file(input_file)
    slideshow: model.Slideshow = solve(photos)
    print(slideshow.score())

    input_name: str = input_file.name.replace(".txt", "")
    output_file: Path = Path.cwd().joinpath(
      "out_do_one", f"out-from_{input_name}-score_{slideshow.score()}.txt"
    )

    slideshow.save(output_file)

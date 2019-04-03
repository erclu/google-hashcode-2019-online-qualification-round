import random
from pathlib import Path
from typing import List, Set

from tqdm import tqdm

from . import model


def _get_horizontal_slides(photos: List[model.Photo]
                           ) -> Set[model.HorizontalSlide]:

    return {
      model.HorizontalSlide(ph)
      for ph in photos
      if ph.orientation == "H"
    }


def _get_vertical_slides(photos: List[model.Photo]
                         ) -> Set[model.VerticalSlide]:
    vertical_photos = set(filter(lambda x: x.orientation == "V", photos))

    vertical_slides: Set[model.VerticalSlide] = set()

    def best_match(
      photo: model.Photo, matches: Set[model.Photo]
    ) -> model.Photo:
        """contains the logic for matching vertical photos into a slide"""
        assert photo

        return random.sample(matches, 1)[0]

    while vertical_photos:
        current: model.Photo = vertical_photos.pop()

        if not vertical_photos:
            break  # handle case with odd number of vertical photos

        other: model.Photo = best_match(current, vertical_photos)

        vertical_photos.remove(other)

        vertical_slides.add(model.VerticalSlide(current, other))

    return vertical_slides


def solve(photos: List[model.Photo]) -> model.Slideshow:

    slides: Set[model.Slide] = _get_horizontal_slides(photos)
    slides.update(_get_vertical_slides(photos))
    print("------------ made slides from photos ------------")

    slideshow: model.Slideshow = model.Slideshow()

    current_slide: model.Slide = random.sample(slides, 1)[0]
    slides.remove(current_slide)

    slideshow.append(current_slide)

    window_size = 5000  # XXX less than 500 gets bad scores
    with tqdm(total=len(slides)) as pbar:
        while slides:
            max_score: int = -1
            best_slide: model.Slide = None

            for next_slide in random.sample(slides, min(window_size,
                                                        len(slides))):
                new_score = current_slide.score(next_slide)
                if new_score > max_score:
                    max_score = new_score
                    best_slide = next_slide

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

    file: Path
    for file in input_files:
        output_file = output_folder/file.name.replace("input", "output")

        photos: List[model.Photo] = model.Photo.from_file(file)

        slideshow: model.Slideshow = solve(photos)

        slideshow.save(output_file)


def do_one(file: str):
    input_file: Path = Path(file).resolve()

    photos: List[model.Photo] = model.Photo.from_file(input_file)
    slideshow: model.Slideshow = solve(photos)
    print(slideshow.score())

    input_name: str = input_file.name.replace(".txt", "")
    output_file: Path = Path.cwd().joinpath(
      "out_do_one", f"out-from_{input_name}-score_{slideshow.score()}.txt"
    )

    slideshow.save(output_file)


#TODO add line_profiler to requirements.txt
def profile_this():
    #TODO implement
    pass

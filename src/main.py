from pathlib import Path
from random import randint
from typing import List

import numpy as np
from tqdm import tqdm

from photo import Photo
from slide import Slide


def parse_file(filename: Path) -> List[str]:
    return filename.read_text().split('\n')[1:-1]


def output(slideshow, out_file):
    file = open(out_file, "w")
    file.write(str(len(slideshow)) + "\n")
    for slide in slideshow:
        file.write(str(slide) + "\n")
    file.close()


def function(set1, set2):
    intersection = len(set1.intersection(set2))
    diff1 = len(set1.difference(set2))
    diff2 = len(set2.difference(set1))
    return min(intersection, diff1, diff2)


def photo_combiner(list_of_pics):
    vertical_pics = []
    slide = []
    for pic in list_of_pics:
        if pic.orientation == 'V':
            vertical_pics.append(pic)
        else:
            slide.append(Slide(pic))

    for i in range(0, len(vertical_pics), 2):
        slide.append(Slide(vertical_pics[i], vertical_pics[i + 1]))
    return slide


def get_slideshow(slides):
    limit = 10
    slideshow = []
    point_list = []
    # bitmask where already picked slides are remembered
    bitmask = np.zeros(len(slides))
    # index of last slide that was added to slideshow
    last_added = randint(0, len(slides))
    slideshow.append(slides[last_added])

    for _ in tqdm(range(len(slides) - 1)):
        max_point = 0
        best_index = -1
        # non taken slides
        valid_indexes = np.nonzero(bitmask - 1)[0]
        # can be done way better with binary search
        last_pos = np.where(valid_indexes == last_added)[0][0]
        # taking 2*limit valid slides to be compared with last slide
        sup_lim = last_pos + limit
        inf_lim = last_pos - limit
        wanted_indexes = np.concatenate(
          (
            valid_indexes[inf_lim:last_pos - 1],
            valid_indexes[last_pos + 1:sup_lim]
          )
        )

        # FIXME
        if len(wanted_indexes) == 0:
            break
        for slide in wanted_indexes:
            points = function(slides[last_added].tags, slides[slide].tags)
            if max_point <= points:
                best_index = slide
                max_point = points
            if max_point == len(slides[last_added].tags) // 2:
                break
        bitmask[last_added] = 1
        point_list.append(max_point)
        slideshow.append(slides[best_index])
        last_added = best_index
    return slideshow, point_list


def check_validity(slideshow, points):
    photos = []
    for slide in slideshow:
        photos += slide.id
    if len(photos) != len(set(photos)):
        return 0
    else:
        return np.sum(points)


def main():
    input_folder: Path = Path(__file__).resolve().parents[1].joinpath("in")
    input_files = input_folder.glob("input*")

    index = 1
    tot_points = []

    for file in input_files:
        lines = parse_file(file)

        photos = [
          Photo.from_str(photoid, value)
          for photoid, value in enumerate(lines)
        ]

        photos.sort(key=lambda x: len(x.tags))

        slides = photo_combiner(photos)
        slideshow, points = get_slideshow(slides)

        tot_points.append(check_validity(slideshow, np.array(points)))
        output(slideshow, "../out/output" + str(index) + ".txt")
        index += 1
    print("\n\n\n\npoints for each input")
    print(*tot_points)


if __name__ == "__main__":
    main()

from __future__ import annotations # ref PEP 563

import typing
from pathlib import Path


def score_tags(first: typing.Set[str], second: typing.Set[str]) -> int:
    common_tags = len(first.intersection(second))
    first_diff = len(first) - common_tags
    second_diff = len(second) - common_tags
    return min(common_tags, first_diff, second_diff)


class Photo:

    def __init__(
      self, photo_id: str, orientation: str, tags: typing.Set[str]
    ) -> None:
        #FIXME SHOULD THIS BE INT?
        self.photo_id = photo_id
        self.orientation = orientation
        self.tags = tags

    def __repr__(self) -> str:
        return str(self.photo_id)

    @classmethod
    def from_str(cls, photo_id: int, line: str) -> Photo:
        args: typing.List[str] = line.split(" ")

        orientation: str = args[0]
        assert orientation in (
          "H", "V"
        ), "orientation was not parsed correctly"

        tags: typing.Set[str] = set(args[2:])
        assert len(tags) == int(args[1]), "not all tags were found"

        return cls(str(photo_id), orientation, tags)

    @staticmethod
    def from_file(filename: Path) -> typing.List[Photo]:
        content = filename.read_text()

        # drop first and last line in file
        photos_lines: typing.List[str] = content.split("\n")[1:-1]

        return [Photo.from_str(pid, x) for pid, x in enumerate(photos_lines)]


class Slide:

    @property
    def tags(self) -> typing.Set[str]:
        raise NotImplementedError

    def score(self, other: Slide) -> int:
        return score_tags(self.tags, other.tags)


class HorizontalSlide(Slide):

    def __init__(self, photo: Photo) -> None:
        assert photo.orientation == "H", (
          "wrong orientation for this slide type"
        )
        self.photo = photo

    def __repr__(self) -> str:
        return str(self.photo.photo_id)

    def __hash__(self) -> int:
        return int(self.photo.photo_id)

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(
          other, HorizontalSlide
        ) and self.photo.photo_id == other.photo.photo_id

    @property
    def tags(self) -> typing.Set[str]:
        return self.photo.tags


class VerticalSlide(Slide):

    def __init__(self, first_photo: Photo, second_photo: Photo) -> None:
        assert (
          first_photo.orientation == "V" and second_photo.orientation == "V"
        ), ("wrong orientation for this slide type")
        self.first: Photo = first_photo
        self.second: Photo = second_photo

    def __repr__(self) -> str:
        return "{} {}".format(self.first, self.second)

    def __hash__(self) -> int:
        return hash((self.first.photo_id, self.second.photo_id))

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, VerticalSlide) and (
          self.first.photo_id, self.second.photo_id
        ) == (other.first.photo_id, other.second.photo_id)

    @property
    def tags(self) -> typing.Set[str]:
        return self.first.tags.union(self.second.tags)


class Slideshow:

    def __init__(self) -> None:
        self.slides: typing.List[Slide] = []
        self._score = 0

    def __repr__(self) -> str:
        return str(self.slides)

    def to_string(self) -> str:
        return "{}\n".format(len(self.slides)
                             ) + "\n".join(str(x) for x in self.slides) + "\n"

    def save(self, filename: Path) -> None:
        filename.write_text(self.to_string(), encoding="UTF-8")

    def append(self, slide: Slide) -> None:
        if self.slides:
            self._score += self.slides[-1].score(slide)
        self.slides.append(slide)

    def score(self) -> int:
        return self._score

    @classmethod
    def from_list(cls, slides_list: typing.List[Slide]) -> Slideshow:
        slideshow = cls()

        for slide in slides_list:
            slideshow.append(slide)

        return slideshow

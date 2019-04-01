from typing import List, Set


def score_tags(first: Set[str], second: Set[str]) -> int:
    common_tags = len(first.intersection(second))
    first_diff = len(first) - common_tags
    second_diff = len(second) - common_tags
    return min(common_tags, first_diff, second_diff)


class Photo:

    def __init__(self, photo_id: str, orientation: str, tags: Set[str]):
        self.photo_id: str = photo_id
        self.orientation: str = orientation
        self.tags: Set[str] = tags

    def __repr__(self):
        return str(self.photo_id)

    @classmethod
    def from_str(cls, photo_id: int, line: str):
        args: List[str] = line.split(" ")

        orientation: str = args[0]
        assert orientation in (
          "H", "V"
        ), "orientation was not parsed correctly"

        tags: Set[str] = set(args[2:])
        assert len(tags) == int(args[1]), "not all tags were found"

        return cls(photo_id, orientation, tags)


class Slide:

    @property
    def tags(self) -> Set[str]:
        pass

    def score(self, other) -> int:
        return score_tags(self.tags, other.tags)


class HorizontalSlide(Slide):

    def __init__(self, photo):
        assert photo.orientation == "H", (
          "wrong orientation for this slide type"
        )
        self.photo = photo

    def __repr__(self):
        return str(self.photo.photo_id)

    @property
    def tags(self) -> Set[str]:
        return self.photo.tags


class VerticalSlide(Slide):

    def __init__(self, first_photo: Photo, second_photo: Photo):
        assert (
          first_photo.orientation == "V" and second_photo.orientation == "V"
        ), ("wrong orientation for this slide type")
        self.first: Photo = first_photo
        self.second: Photo = second_photo

    def __repr__(self):
        return f"{self.first} {self.second}"

    @property
    def tags(self) -> Set[str]:
        return self.first.tags.union(self.second.tags)


class Slideshow:

    def __init__(self):
        self.slides: List[Slide] = []
        self._score = 0

    def __repr__(self):
        return str(self.slides)

    def to_string(self) -> str:
        return f"{len(self.slides)}\n" + "\n".join(
          str(x) for x in self.slides
        ) + "\n"

    def append(self, slide: Slide) -> None:
        if self.slides:
            self._score += self.slides[-1].score(slide)
        self.slides.append(slide)

    def score(self) -> int:
        return self._score

    @classmethod
    def from_list(cls, slides_list):
        slideshow = cls()

        for slide in slides_list:
            slideshow.append(slide)

        return slideshow

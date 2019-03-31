from typing import Set, List


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


class HorizontalSlide:

    def __init__(self, photo):
        assert photo.orientation == "H", (
          "wrong orientation for this slide type"
        )
        self.photo = photo

    def __repr__(self):
        return self.photo.photo_id

    @property
    def tags(self) -> Set[str]:
        return self.photo.tags

    def score(self, other) -> int:
        #TODO scoring function
        pass


class VerticalSlide:

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

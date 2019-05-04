import re
import typing
from pathlib import Path

import pytest

OUTPUT_FOLDER: Path = Path(__file__
                           ).resolve().parents[1].joinpath("out_do_one")
SUBMITTED_OUTPUT_FOLDER: Path = OUTPUT_FOLDER.parent.joinpath(
  "submitted_outputs"
)
INPUT_FOLDER: Path = OUTPUT_FOLDER.parent.joinpath("in")


def compare_input_output_files(input_file: Path, output_file: Path):
    infile: typing.TextIO
    with input_file.open("r") as infile:
        declared_input_photos_number: int = int(infile.readline())
        input_photos: typing.List[str] = infile.readlines()

    input_photos_number = len(input_photos)

    vertical_input_photos_number = 0
    horizontal_input_photos_number = 0

    for x in input_photos:
        if x[0] == "V":
            vertical_input_photos_number += 1
        elif x[0] == "H":
            horizontal_input_photos_number += 1
        else:
            raise ValueError

    assert declared_input_photos_number == input_photos_number
    assert (
      vertical_input_photos_number +
      horizontal_input_photos_number == input_photos_number
    )

    outfile: typing.TextIO
    with output_file.open("r") as outfile:
        declared_slides_number = int(outfile.readline())
        lines: typing.List[str] = outfile.readlines()

    output_slides_number = len(lines)

    assert declared_slides_number == output_slides_number
    assert output_slides_number <= input_photos_number

    output_photos_number = 0
    vertical_output_photos_number = 0
    horizontal_output_photos_number = 0

    for x in lines:
        current_photos_number: str = len(x.split(" "))
        output_photos_number += current_photos_number

        if current_photos_number > 1:
            vertical_output_photos_number += current_photos_number
        else:
            horizontal_output_photos_number += current_photos_number

    assert output_photos_number == input_photos_number
    assert (
      vertical_output_photos_number +
      horizontal_output_photos_number == output_photos_number
    )


@pytest.mark.parametrize("output_file", OUTPUT_FOLDER.glob("out-from*.txt"))
def test_output_file(output_file: Path):
    input_file: Path = Path(
      INPUT_FOLDER,
      re.sub(
        r'-score_\d+\.txt', ".txt", output_file.name.replace("out-from_", "")
      )
    )
    assert input_file.exists()

    compare_input_output_files(input_file, output_file)


@pytest.mark.parametrize(
  "submitted_output_file", SUBMITTED_OUTPUT_FOLDER.glob("output*.txt")
)
@pytest.mark.skip(reason="results never change")
def test_submitted_output(submitted_output_file):
    input_file: Path = Path(
      INPUT_FOLDER,
      re.sub(
        r'-\d+\.txt', ".txt",
        submitted_output_file.name.replace("output", "input")
      )
    )
    assert input_file.exists()

    compare_input_output_files(input_file, submitted_output_file)


# assert output_photos_number == input_photos_number
# assert                78801 == 80000
# assert                  999 == 1000
# assert                89999 == 90000

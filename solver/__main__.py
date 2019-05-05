import sys
from pathlib import Path

from solver.solve import do_one, profile_me

# TODO use mypy!
# FIXME not sure this is right
if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "profile":
            profile_me()
            exit()

        files_list = sys.argv[1:]
    else:
        input_folder: Path = Path(__file__).resolve().parents[1].joinpath("in")
        files_list = [str(x) for x in input_folder.glob("input*")]

    for file in files_list:
        do_one(file)

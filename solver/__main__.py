import sys

from solver.solve import do_one

if __name__ == "__main__":
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        raise ValueError("wrong cli arguments")

    file = sys.argv[1]

    if len(sys.argv) == 3:
        do_one(file, int(sys.argv[2]))
    else:
        do_one(file)

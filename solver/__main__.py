import sys

if __name__ == "__main__":
    from solver.solve import do_one, do_all

    if sys.argv[1]:
        do_one(sys.argv[1])
    else:
        do_all()

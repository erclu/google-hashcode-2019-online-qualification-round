import sys

# FIXME not sure this is right
if __name__ == "__main__":
    from solver.solve import do_one, do_all

    if len(sys.argv) == 2:
        do_one(sys.argv[1])
    else:
        do_all()

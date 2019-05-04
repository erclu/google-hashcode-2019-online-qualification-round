import sys

# TODO use mypy!
# FIXME not sure this is right
if __name__ == "__main__":
    from solver.solve import do_one, do_all

    if len(sys.argv) > 1:
        files_list = sys.argv[1:]
        for file in files_list:
            do_one(file)
    else:
        do_all()

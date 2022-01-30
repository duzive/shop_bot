import os
import sys


def reload():
    python = sys.executable
    os.execl(python, python, "{}".format(sys.argv[0]))

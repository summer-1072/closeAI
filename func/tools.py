import os
import shutil


def remove_files(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)

        if os.path.isdir(path):
            shutil.rmtree(path)

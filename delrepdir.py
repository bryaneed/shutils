
import os
import shutil


def remove_dirs(dir_name):
    for files in os.listdir(dir_name):
        if os.path.isdir(files):
            codir = os.path.join(dir_name, files, files)
            print(codir)
            if os.path.exists(codir):
                try:
                    os.removedirs(codir)
                except OSError:
                    shutil.rmtree(codir)


if __name__ == '__main__':
    remove_dirs(os.path.dirname(os.path.abspath(__file__)))

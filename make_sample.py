"""make_sample.py - create a made-up practice folder for the lesson.

Creates a folder called "sample" next to this script with made-up
files in a small nested shape. Run it again any time; it first
removes the old sample folder.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "sample")

FILES = [
    "notes.txt",
    "photos/cat.jpg",
    "photos/dog.jpg",
    "photos/raw/cat-01.png",
    "reports/january.txt",
    "reports/february.txt",
    "todo.txt",
]


def main():
    if os.path.isdir(SAMPLE):
        shutil.rmtree(SAMPLE)
    for relative in FILES:
        path = os.path.join(SAMPLE, *relative.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as handle:
            handle.write("made-up practice bytes\n")
    print("Sample folder ready: " + SAMPLE)
    print("It holds 7 made-up files in 3 folders.")


if __name__ == "__main__":
    main()

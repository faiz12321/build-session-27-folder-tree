"""treeprint.py - print the shape of a folder as an indented tree.

Read-only: it only looks. It never changes, moves or deletes anything.

Each level is indented two spaces. Names are sorted letter by letter,
ignoring letter case. Folders and files appear mixed in name order.
Unsafe aliases and read/metadata errors refuse.

Usage:
    python treeprint.py [FOLDER]
FOLDER defaults to the current folder.
"""
import os
import sys
import stat
from pathlib import Path


def safe_input(value, directory=False):
    path = Path(value).absolute()
    if '..' in path.parts:
        raise OSError('Parent-traversal paths are unsupported.')
    for part in [*reversed(path.parents), path]:
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise OSError('Links/reparse points are unsupported.')
    info = path.lstat()
    if directory:
        if not stat.S_ISDIR(info.st_mode):
            raise NotADirectoryError('Expected an ordinary directory.')
    elif not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise OSError('Expected an ordinary singly linked file.')
    return path







def walk_tree(root):
    """Return (lines, folder_count, file_count) for the tree under
    root. Lines hold (depth, name) pairs; the root itself is not a
    line. Unsafe aliases and read/metadata errors refuse."""
    safe_input(root, directory=True)
    lines = []
    folders = 0
    files = 0

    def visit(path, depth):
        nonlocal folders, files
        try:
            names = sorted(os.listdir(path), key=str.lower)
        except OSError:
            raise
        for name in names:
            full = os.path.join(path, name)
            info = Path(full).lstat()
            directory = stat.S_ISDIR(info.st_mode)
            safe_input(full, directory=directory)
            if directory:
                lines.append((depth, name + "/"))
                folders += 1
                visit(full, depth + 1)
            else:
                lines.append((depth, name))
                files += 1

    visit(root, 0)
    return lines, folders, files


def main(argv):
    if len(argv) > 2 or (len(argv) == 2 and argv[1] in ("-h", "--help")):
        print("Usage: python treeprint.py [FOLDER]", file=sys.stderr)
        return 2
    root = argv[1] if len(argv) == 2 else "."
    try:
        safe_input(root, directory=True)
    except OSError as error:
        print("No such folder: " + root + " (" + str(error) + ")", file=sys.stderr)
        return 2
    if not os.path.isdir(root):
        print("No such folder: " + root, file=sys.stderr)
        return 2
    try:
        lines, folders, files = walk_tree(root)
    except OSError as error:
        print("Could not complete tree: " + str(error), file=sys.stderr)
        return 2
    print("Folder tree")
    print("Folder: " + root)
    print()
    for depth, name in lines:
        print("  " * depth + name)
    print()
    print("Folders: " + str(folders) + ", files: " + str(files))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

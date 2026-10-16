"""treeprint.py - print the shape of a folder as an indented tree.

Read-only: it only looks. It never changes, moves or deletes anything.

Each level is indented two spaces. Names are sorted letter by letter,
ignoring letter case. Folders and files appear mixed in name order.
Unreadable folders are skipped.

Usage:
    python treeprint.py [FOLDER]
FOLDER defaults to the current folder.
"""
import os
import sys


def walk_tree(root):
    """Return (lines, folder_count, file_count) for the tree under
    root. Lines hold (depth, name) pairs; the root itself is not a
    line. Unreadable folders are skipped."""
    lines = []
    folders = 0
    files = 0

    def visit(path, depth):
        nonlocal folders, files
        try:
            names = sorted(os.listdir(path), key=str.lower)
        except OSError:
            return
        for name in names:
            full = os.path.join(path, name)
            if os.path.isdir(full):
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
    if not os.path.isdir(root):
        print("No such folder: " + root, file=sys.stderr)
        return 2
    lines, folders, files = walk_tree(root)
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

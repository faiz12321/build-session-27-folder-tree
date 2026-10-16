# Folder tree printer

`treeprint.py` prints the shape of a folder as an indented tree, so
you can see at a glance what sits inside what. It is read-only: it
only looks, and it never changes, moves or deletes anything. Run it
first on the made-up `sample` folder from `make_sample.py` before
pointing it anywhere else.

- Each level is indented two spaces; folder names end with a slash.
- Names are sorted letter by letter, ignoring letter case.
- Folders the tool cannot read are skipped; the report only covers
  what it could see.
- The report shows names only, never what is inside files. A big or
  deep folder makes a long report.

## Use

    python make_sample.py
    python treeprint.py sample
    python treeprint.py "C:\Users\you\Documents"

If you leave out the folder, the current folder is printed.

## Tests

    python -m unittest -v

Works on Windows, Mac and Linux with Python 3.10 or newer. Nothing to
install: it uses only what comes with Python.

## License

MIT (see LICENSE).

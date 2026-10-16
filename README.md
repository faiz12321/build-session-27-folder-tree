# Print a folder tree

Read-only teaching tool: print file and folder names with two-space indentation,
sorted ignoring case. Names only, never file contents. Unreadable folders can
be skipped. The report is not proof of completeness or deletion safety.

## Link limitation

The tree printer follows directory symlinks and junctions without cycle
detection. Links can lead outside the chosen tree or repeat a loop. Use only
the small link-free practice sample, not a real folder tree. This setup repair
does not change link handling.

## Practise

Save all three files in a new empty lesson folder. Python 3 is required:

    python make_sample.py
    python treeprint.py sample
    python treeprint.py sample/photos
    python -m unittest -v

Setup creates sample beside its script and refuses any existing sample path.
It never deletes, replaces or resets an old sample. Use a different new empty
lesson folder if it refuses. Photo names contain fictional text practice bytes,
not real photos.

## Evidence

20 tests use temporary fixtures, including the sample-count test. They cover
tree shape, sorted paths, CLI errors, unchanged source metadata, setup refusal
for an existing file/folder, original bytes, a nested unrelated file and repeat
run preservation. These limited fixture checks do not prove universal safety.

The revised lesson was recorded twice on GitHub-hosted Windows and twice on
Ubuntu. The driver saves the top-level list first, records it, then saves the
final recursive tree printer, matching the lesson stages. Displayed output is
the first Windows run. Paired platform runs differ only in unittest elapsed
time. Versions and test rendering may differ. No Windows desktop or macOS
session was tested.

## License

MIT (see LICENSE).

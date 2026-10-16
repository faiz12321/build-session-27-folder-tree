# Print a fictional folder tree

Save three source files in a NEW empty lesson folder.

    python make_sample.py
    python treeprint.py sample
    python -m unittest -v

Two Windows and two Ubuntu full replays run exact visible source versions. Final 34 small fixture tests pass (Unix pipe skips on Windows); symlink creation can skip where unavailable. Displayed stdout is first Windows output, not normalized or mixed. Pair differences are unittest time.
Link/error changes only: refuse root/ancestor and traversed tree symbolic links/reparse points, hardlinks, special entries and traversal before recursive visits. Read/list/metadata errors now stop with exit 2 instead of silent skips, false clean totals or alias loops. Setup refuses linked parents/traversal and existing sample paths, without reset or deletion. Naive first version remains fictional-sample-only and must be replaced.
Original recursive folder shape, two-space indentation, mixed file/folder lowercased name ordering, relative root label and counts remain unchanged. Recursive implementation and case-tie behavior remain unchanged. Very deep trees can still reach Python's recursion limit, and large trees consume memory. No size/depth/time limit was added.
The checker has no write/move/delete/network code and opens no file contents. No atomic snapshot or hostile-race defense. Stop editors/sync; entries can change during traversal. Filenames and paths can be private. Small fictional fixtures are not proof on every filesystem. No desktop Windows/macOS recording. Recorder removes only its own temporary fixture folder. Decisions and feedback are teaching text, not recorded output.

MIT code. Python separately licensed/not included.

Reference: https://docs.python.org/3/library/os.html

Windows pair: https://github.com/faiz12321/lesson-lab/actions/runs/38975821494
Ubuntu pair: https://github.com/faiz12321/lesson-lab/actions/runs/38975878430

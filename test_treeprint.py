"""Tests for treeprint.py."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "treeprint.py")
sys.path.insert(0, HERE)
import treeprint


def run_tool(*args, cwd=None):
    return subprocess.run(
        [sys.executable, TOOL] + list(args),
        capture_output=True, text=True, timeout=60, cwd=cwd,
    )


def make(root, relative, text="x"):
    path = os.path.join(root, *relative.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as handle:
        handle.write(text)


def snapshot_tree(root):
    snap = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            full = os.path.join(dirpath, name)
            st = os.stat(full)
            snap.append((full, st.st_size, st.st_mtime_ns))
    return sorted(snap)


class WalkTreeTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_empty_folder_has_no_lines(self):
        lines, folders, files = treeprint.walk_tree(self.root)
        self.assertEqual(lines, [])
        self.assertEqual((folders, files), (0, 0))

    def test_files_and_folders_are_counted(self):
        make(self.root, "a.txt")
        make(self.root, "sub/b.txt")
        lines, folders, files = treeprint.walk_tree(self.root)
        self.assertEqual((folders, files), (1, 2))

    def test_nested_folder_indents_one_more_level(self):
        make(self.root, "sub/inner/deep.txt")
        lines, folders, files = treeprint.walk_tree(self.root)
        self.assertEqual(
            lines,
            [(0, "sub/"), (1, "inner/"), (2, "deep.txt")],
        )

    def test_names_sort_letter_by_letter(self):
        make(self.root, "b.txt")
        make(self.root, "a.txt")
        lines, folders, files = treeprint.walk_tree(self.root)
        self.assertEqual(lines, [(0, "a.txt"), (0, "b.txt")])

    def test_sorting_ignores_letter_case(self):
        make(self.root, "Banana.txt")
        make(self.root, "apple.txt")
        lines, folders, files = treeprint.walk_tree(self.root)
        self.assertEqual(lines, [(0, "apple.txt"), (0, "Banana.txt")])

    def test_folders_appear_in_name_order_with_files(self):
        make(self.root, "middle.txt")
        make(self.root, "alpha/x.txt")
        make(self.root, "zulu.txt")
        lines, folders, files = treeprint.walk_tree(self.root)
        names = [name for depth, name in lines]
        self.assertEqual(names, ["alpha/", "x.txt", "middle.txt", "zulu.txt"])

    def test_folder_names_end_with_a_slash(self):
        make(self.root, "sub/x.txt")
        lines, folders, files = treeprint.walk_tree(self.root)
        self.assertEqual(lines[0], (0, "sub/"))


class CliTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_report_indents_the_tree(self):
        make(self.root, "photos/cat.jpg")
        make(self.root, "photos/raw/cat-01.png")
        make(self.root, "notes.txt")
        result = run_tool(self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        body = result.stdout
        self.assertIn("notes.txt", body)
        self.assertIn("photos/", body)
        self.assertIn("  cat.jpg", body)
        self.assertIn("  raw/", body)
        self.assertIn("    cat-01.png", body)
        self.assertIn("Folders: 2, files: 3", body)

    def test_report_shows_folder_as_given(self):
        with tempfile.TemporaryDirectory() as work:
            make(work, "sample/a.txt")
            result = run_tool("sample", cwd=work)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Folder: sample", result.stdout)

    def test_missing_folder_is_a_clear_error(self):
        result = run_tool(os.path.join(self.root, "nope"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("No such folder", result.stderr)

    def test_file_instead_of_folder_is_a_clear_error(self):
        make(self.root, "notes.txt")
        result = run_tool(os.path.join(self.root, "notes.txt"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("No such folder", result.stderr)

    def test_too_many_arguments_prints_usage(self):
        result = run_tool("a", "b", "c")
        self.assertEqual(result.returncode, 2)
        self.assertIn("python treeprint.py", result.stderr)

    def test_help_prints_usage(self):
        result = run_tool("--help")
        self.assertEqual(result.returncode, 2)
        self.assertIn("python treeprint.py", result.stderr)

    def test_folder_defaults_to_current_folder(self):
        make(self.root, "a.txt")
        result = run_tool(cwd=self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Folders: 0, files: 1", result.stdout)

    def test_tool_does_not_change_the_tree(self):
        make(self.root, "photos/cat.jpg")
        make(self.root, "notes.txt")
        before = snapshot_tree(self.root)
        result = run_tool(self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        after = snapshot_tree(self.root)
        self.assertEqual(before, after)


class SampleTests(unittest.TestCase):
    def test_sample_folder_matches_the_lesson_counts(self):
        sample = os.path.join(HERE, "sample")
        if not os.path.isdir(sample):
            self.skipTest("sample folder not made yet")
        lines, folders, files = treeprint.walk_tree(sample)
        self.assertEqual((folders, files), (3, 7))
        self.assertEqual(lines[0], (0, "notes.txt"))
        self.assertIn((2, "cat-01.png"), lines)


class SafetyTests(unittest.TestCase):
    def test_source_has_no_write_calls(self):
        with open(TOOL) as handle:
            source = handle.read()
        for banned in ("shutil", "os.remove", "os.rmdir", "os.rename",
                       "os.makedirs", "open("):
            self.assertNotIn(banned, source)


if __name__ == "__main__":
    unittest.main()

import tempfile
from pathlib import Path
import unittest

from noteeds.engine.repository import FileEntry, Repository


class RepositoryTest(unittest.TestCase):
    def test_something(self):
        with tempfile.TemporaryDirectory() as repo_dir:
            repo_path = Path(repo_dir)

            # TODO test repo path: file, symlink to file, symlink to directory,
            # nonexistent, broken symlink
            # TODO test in repo: symlink to file, symlink to directory, broken
            # symlink

            (repo_path / "foo").touch()
            (repo_path / "bar").touch()
            (repo_path / ".dot").touch()
            (repo_path / "subdir").mkdir()
            (repo_path / "subdir" / "subfoo").touch()
            (repo_path / ".dotdir").mkdir()
            (repo_path / ".dotdir" / ".dotfoo").touch()

            repo = Repository(repo_path)

            self.assertSetEqual({
                FileEntry(repo_path / "foo"),
                FileEntry(repo_path / "bar"),
            }, set(repo.entries()))


if __name__ == '__main__':
    unittest.main()

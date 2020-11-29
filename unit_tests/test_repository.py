import tempfile
from pathlib import Path
import unittest

from noteeds.engine.repository import FileEntry, Repository, Config as RepositoryConfig


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
            (repo_path / "sub_dir").mkdir()
            (repo_path / "sub_dir" / "sub_foo").touch()
            (repo_path / ".dot_dir").mkdir()
            (repo_path / ".dot_dir" / ".dot_foo").touch()

            repo = Repository(RepositoryConfig(None, repo_path, None, True))

            self.assertSetEqual({
                FileEntry(repo_path / "foo", Repository),
                FileEntry(repo_path / "bar", Repository),
            }, set(repo.entries()))


if __name__ == '__main__':
    unittest.main()

from pathlib import Path
import unittest
import tempfile

from noteeds.util.io import read_file


class IoTest(unittest.TestCase):
    def test_read_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "file"

            file_path.write_bytes(b"foo\xB2")
            self.assertEqual(("foo²", "latin1"), read_file(file_path))

            file_path.write_bytes(b"foo\xC2\xB2")
            self.assertEqual(("foo²", "utf-8"), read_file(file_path))


if __name__ == '__main__':
    unittest.main()

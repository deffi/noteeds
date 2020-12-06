import unittest

from noteeds.util import MultiFormatter


class MultiFormatterTest(unittest.TestCase):
    def test_unused(self):
        f = MultiFormatter(11, 22, foo=33, bar=44)
        self.assertSetEqual({0, 1, "foo", "bar"}, f.unused)

        self.assertEqual("33: 22", f.format("{foo}: {1}"))
        self.assertSetEqual({0, "bar"}, f.unused)

        self.assertEqual("33: 11", f.format("{foo}: {0}"))
        self.assertSetEqual({"bar"}, f.unused)

        self.assertEqual("44: 22", f.format("{bar}: {1}"))
        self.assertSetEqual(set(), f.unused)


if __name__ == '__main__':
    unittest.main()

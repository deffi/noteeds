import unittest

from noteeds.util import Formatter


class FormatterTest(unittest.TestCase):
    def test_unused(self):
        f = Formatter()

        # All args
        self.assertEqual("11: 33", f.format("{0}: {2}", 11, 22, 33))
        self.assertSetEqual({1}, f.unused)

        # All kwargs
        self.assertEqual("11: 33", f.format("{foo}: {baz}", foo=11, bar=22, baz=33))
        self.assertSetEqual({"bar"}, f.unused)

        # Mixed
        self.assertEqual("33: 22", f.format("{foo}: {1}", 11, 22, foo=33, bar=44))
        self.assertSetEqual({"bar", 0}, f.unused)


if __name__ == '__main__':
    unittest.main()

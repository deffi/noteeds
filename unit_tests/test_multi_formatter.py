import unittest

from noteeds.util import MultiFormatter


class MultiFormatterTest(unittest.TestCase):
    # TODO test with "{}"

    def test_format_field(self):
        # TODO test conversion, need a string value

        f = MultiFormatter(11, 22, foo=33, bar=44)

        # All fields are unused
        self.assertSetEqual({0, 1, "foo", "bar"}, f.unused)

        # Access all fields without using them
        self.assertEqual("11", f.format_field(0, use=False))
        self.assertEqual("22", f.format_field(1, use=False))
        self.assertEqual("33", f.format_field("foo", use=False))
        self.assertEqual("44", f.format_field("bar", use=False))

        # All fields are still unused
        self.assertSetEqual({0, 1, "foo", "bar"}, f.unused)

        # Access all fields using them; they will no longer be unused
        self.assertEqual("11", f.format_field(0))
        self.assertSetEqual({1, "foo", "bar"}, f.unused)
        self.assertEqual("33", f.format_field("foo"))
        self.assertSetEqual({1, "bar"}, f.unused)
        self.assertEqual("22", f.format_field(1))
        self.assertSetEqual({"bar"}, f.unused)
        self.assertEqual("44", f.format_field("bar"))
        self.assertSetEqual(set(), f.unused)

        # But we can access them again (this time with format spec)
        self.assertEqual("011", f.format_field(0, "03d"))
        self.assertEqual("033", f.format_field("foo", "03d"))

        # Accessing them without using doesn't make them unused again
        self.assertEqual("11", f.format_field(0, use=False))
        self.assertSetEqual(set(), f.unused)

    def test_format(self):
        f = MultiFormatter(11, 22, foo=33, bar=44)
        self.assertSetEqual({0, 1, "foo", "bar"}, f.unused)

        # Access without using
        self.assertEqual("33: 22", f.format("{foo}: {1}", use=False))
        self.assertSetEqual({0, 1, "foo", "bar"}, f.unused)

        # Access
        self.assertEqual("33: 22", f.format("{foo}: {1}"))
        self.assertSetEqual({0, "bar"}, f.unused)

        # Access
        self.assertEqual("33: 11", f.format("{foo}: {0}"))
        self.assertSetEqual({"bar"}, f.unused)

        # Access
        self.assertEqual("44: 22", f.format("{bar}: {1}"))
        self.assertSetEqual(set(), f.unused)


if __name__ == '__main__':
    unittest.main()

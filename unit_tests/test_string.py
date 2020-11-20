import unittest

from noteeds.util.string import map_lines, strip_lines, box


class StringTest(unittest.TestCase):
    def test_map_lines(self):
        value = "Foo\nBar\nBaz"
        self.assertEqual("FooFoo\nBarBar\nBazBaz", map_lines(lambda x: x*2, value))
        self.assertEqual("foo\nbar\nbaz", map_lines(str.lower, value))

    def test_strip_lines(self):
        value = """
            Foo
            Bar
            Baz
        """
        self.assertEqual("Foo\nBar\nBaz", strip_lines(value).strip())

    def test_box(self):
        self.assertEqual([
            "**********",
            "** Test **",
            "**********"], box("Test", "*"))

        self.assertEqual([
            "########",
            "# Test #",
            "########"], box("Test", "#", border_width=1))


if __name__ == '__main__':
    unittest.main()

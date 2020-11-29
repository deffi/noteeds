import unittest

from noteeds.util.iterable import pairs, sequence_join


class IterableTest(unittest.TestCase):
    def test_pairs(self):
        self.assertEqual([(1, 2), (2, 3), (3, 4)], list(pairs([1, 2, 3, 4])))
        self.assertEqual([(1, 2)], list(pairs([1, 2])))
        self.assertEqual([], list(pairs([1])))
        self.assertEqual([], list(pairs([])))

    def test_sequence_join(self):
        self.assertEqual([1, 2, 3, 11, 22, 4, 5, 11, 22], list(sequence_join([11, 22], [[1, 2, 3], [4, 5], []])))


if __name__ == '__main__':
    unittest.main()

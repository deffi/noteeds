import re
import unittest

from noteeds.engine import Query

class QueryTest(unittest.TestCase):
    def test_effecitve_regex(self):
        self.assertEqual(r"foo", Query("foo", False, None, 0).effective_regex)
        self.assertEqual(r"foo", Query("foo", True , None, 0).effective_regex)

        self.assertEqual(r"\[bar\]", Query("[bar]", False, None, 0).effective_regex)
        self.assertEqual(r"[bar]"  , Query("[bar]", True , None, 0).effective_regex)

    def test_effective_case_sensitive(self):
        for text in ["", "f", "foo", "foo42"]:
            self.assertEqual(False, Query(text, False, False).effective_case_sensitive)
            self.assertEqual(True , Query(text, False, True ).effective_case_sensitive)
            self.assertEqual(False, Query(text, False, None ).effective_case_sensitive)

        for text in ["F", "Foo", "foO", "foo42B"]:
            self.assertEqual(False, Query(text, False, False).effective_case_sensitive)
            self.assertEqual(True , Query(text, False, True ).effective_case_sensitive)
            self.assertEqual(True , Query(text, False, None ).effective_case_sensitive)

    def test_effective_flags(self):
        # Without flags, re.I is added for case-insensitive queries
        self.assertEqual(0   , Query("foo", False, True , 0).effective_flags)
        self.assertEqual(re.I, Query("foo", False, False, 0).effective_flags)

        # If re.I is present, it is ignored
        self.assertEqual(0   , Query("foo", False, True , re.I).effective_flags)
        self.assertEqual(re.I, Query("foo", False, False, re.I).effective_flags)

        # If other flags are present, they are mixed in
        self.assertEqual(re.M       , Query("foo", False, True , re.M).effective_flags)
        self.assertEqual(re.M | re.I, Query("foo", False, False, re.M).effective_flags)


if __name__ == '__main__':
    unittest.main()

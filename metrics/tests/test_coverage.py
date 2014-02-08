import os
from unittest import TestCase
from ddt import ddt, unpack, data
from ..coverage import CoverageData, CoverageParseError


@ddt
class CoverageTest(TestCase):

    def setUp(self):
        self.data = CoverageData()

    @data(
        ['simple.xml', '*', 84.615384615385],
        ['simple.xml', 'group_1/*.py', 83.333333333333],
        ['simple.xml', 'group_2/*.py', 85.714285714286],
        ['simple.xml', 'none', None],
        ['missing_filename.xml', '*.py', 84.615384615385],
        ['unicode_filename.xml', '*.py', 84.615384615385],
        ['missing_line_root.xml', '*.py', 84.615384615385],
        ['missing_line_hits.xml', '*.py', 84.61538461538461],
        ['missing_line_num.xml', '*.py', 84.61538461538461],
        ['non_int_hits.xml', '*.py', 84.61538461538461],
        ['non_int_line_num.xml', '*.py', 84.61538461538461]
    )
    @unpack
    def test_add_report(self, report_name, pattern, expected_coverage):
        self.data.add_report(self._report_fixture('simple.xml'))
        actual = self.data.coverage(pattern)

        if expected_coverage is not None:
            self.assertAlmostEqual(actual, expected_coverage, places=3)
        else:
            self.assertIs(actual, None)

    def test_report_overlap(self):
        self.data.add_report(self._report_fixture('overlap_1.xml'))
        self.data.add_report(self._report_fixture('overlap_2.xml'))
        self.assertAlmostEqual(self.data.coverage('group_1/*.py'), 83.333333333333, places=3)

    def test_invalid_xml(self):
        with self.assertRaises(CoverageParseError):
            self.data.add_report(self._report_fixture('invalid.xml'))

    def test_unicode_pattern(self):
        self.data.add_report(self._report_fixture('simple.xml'))
        self.assertIs(self.data.coverage(u'\u9202.py'), None)

    @staticmethod
    def _report_fixture(name):
        """
        Load the fixture with filename `name` and return the contents as a `str`.
        """
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", name)
        with open(path) as fixture_file:
            return fixture_file.read()

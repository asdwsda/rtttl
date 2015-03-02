import unittest
from rtttl.parser import remove_whitespaces, correct_note_syntax

class ParserTest(unittest.TestCase):

    def test_removing_whitespaces(self):
        self.assertEqual(remove_whitespaces(' 16d4, f#  , d . '), '16d4,f#,d.')

    def test_note_syntax_correction(self):
        cases = [
            {'note': 'p', 'expected': 'p'},
            {'note': '4e', 'expected': '4e'},
            {'note': 'd4', 'expected': 'd4'},
            {'note': 'd.', 'expected': 'd.'},
            {'note': 'd4.', 'expected': 'd4.'},
            {'note': 'd.4', 'expected': 'd4.'},
            {'note': '16f', 'expected': '16f'},
            {'note': '16f.', 'expected': '16f.'},
            {'note': '8d.6', 'expected': '8d6.'},
            {'note': '8g#.6', 'expected': '8g#6.'},
            {'note': '8g#5.', 'expected': '8g#5.'},
        ]
        for case in cases:
            self.assertEqual(correct_note_syntax(case['note']), case['expected'])

if __name__ == 'main':
    unittest.main()

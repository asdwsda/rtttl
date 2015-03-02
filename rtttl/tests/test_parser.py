import unittest
from rtttl.parser import remove_whitespaces, correct_note_syntax, parse_note, parse_defaults
from rtttl.exceptions import InvalidDefaults, InvalidNote

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

    def test_parsing_valid_notes(self):
        cases = [
            {'note': 'f',      'expected': {'duration': None, 'octave': None, 'pitch': 'f',  'dot': False}},
            {'note': 'g#',     'expected': {'duration': None, 'octave': None, 'pitch': 'g#', 'dot': False}},
            {'note': '16p',    'expected': {'duration': 16,   'octave': None, 'pitch': 'p',  'dot': False}},
            {'note': 'a7.',    'expected': {'duration': None, 'octave': 7,    'pitch': 'a',  'dot': True}},
            {'note': 'd.',     'expected': {'duration': None, 'octave': None, 'pitch': 'd',  'dot': True}},
            {'note': '8c4',    'expected': {'duration': 8,    'octave': 4,    'pitch': 'c',  'dot': False}},
            {'note': '32a#7.', 'expected': {'duration': 32,   'octave': 7,    'pitch': 'a#', 'dot': True}},
            {'note': '1a#4',   'expected': {'duration': 1,    'octave': 4,    'pitch': 'a#', 'dot': False}},
        ]
        for case in cases:
            self.assertDictEqual(parse_note(case['note']), case['expected'])


    def test_parsing_invalid_notes(self):
        cases = ['', 'j', '66f#', '324g', 'f32', 'a.3', 'krtek', '#', 'a9', '16hb', '4f#6f']
        for case in cases:
            self.assertRaises(InvalidNote, parse_note, case)

    def test_parsing_valid_defaults(self):
        cases = [
            {'defaults': '', 'expected': {'duration': 4, 'octave': 6, 'bpm': 63}},
            {'defaults': 'd=4,o=6,b=63', 'expected': {'duration': 4, 'octave': 6, 'bpm': 63}},
            {'defaults': 'd=16,o=5,b=900', 'expected': {'duration': 16, 'octave': 5, 'bpm': 900}},
        ]

        for case in cases:
            self.assertDictEqual(parse_defaults(case['defaults']), case['expected'])


    def test_parsing_invalid_defaults(self):
        cases = [
            'd=4,o=6,b=0',
            'd=4,o=0,b=63',
            'd=0,o=6,b=63',
            'o=0,d=6,b=63',
            'd=0,o=6,b=63,o=7',
            'd=0,o=6,b=63,c=7',
            'd=0,o=6,c=63',
            'd=0,b=63',
        ]

        for case in cases:
            self.assertRaises(InvalidDefaults, parse_defaults, case)

if __name__ == 'main':
    unittest.main()

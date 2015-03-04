import unittest
from rtttl.parser import remove_whitespaces, correct_note_syntax, parse_note, parse_defaults, parse_rtttl, convert_note
from rtttl.exceptions import InvalidDefaults, InvalidNote, InvalidRTTTLFormat

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

    def test_note_conversion(self):
        defaults = {'duration': 4, 'octave': 6, 'bpm': 63}
        cases = [
            {'note': {'duration': 8, 'pitch': 'f#', 'octave': 5, 'dot': False},
             'expected': {'duration': 476.19, 'frequency': 740.0}},

            {'note': {'duration': 32, 'pitch': 'd', 'octave': 7, 'dot': False},
             'expected':  {'duration': 119.048, 'frequency': 2349.6}},

            {'note': {'duration': 8, 'pitch': 'p', 'octave': None, 'dot': False},
             'expected': {'duration': 476.19, 'frequency': 0}},

            {'note': {'duration': 16, 'pitch': 'c', 'octave': None, 'dot': True},
             'expected': {'duration': 357.143, 'frequency': 1046.4}},

            {'note': {'duration': None, 'pitch': 'c#', 'octave': None, 'dot': False},
             'expected': {'duration': 952.381, 'frequency': 1108.8}},

            {'note': {'duration': None, 'pitch': 'b', 'octave': 5, 'dot': False},
             'expected': {'duration': 952.381, 'frequency': 987.8}},

            {'note': {'duration': None, 'pitch': 'd', 'octave': None, 'dot': True},
             'expected': {'duration': 1428.571, 'frequency': 1174.8}},

            {'note': {'duration': 8, 'pitch': 'd#', 'octave': 6, 'dot': True},
             'expected': {'duration': 714.286, 'frequency': 1244.4}},
        ]

        for case in cases:
            parsed = convert_note(case['note'], defaults)
            self.assertDictEqual(parsed, case['expected'])

    def test_parsing_valid_rtttl_with_whitespaces(self):
        barbie_girl_with_whitespaces = ('Barbie Girl:d=8, o=5, b=125:g#, e, g#, c#6, 4a, 4p, f#, d#, f#, b, 4g#, '
                                        'f#, e, 4p, e, c#, 4f#, 4c#, 4p, f#, e, 4g#, 4f#')

        expected = {'title': 'Barbie Girl',
                    'notes': [{'duration': 240.0, 'frequency': 830.6},
                              {'duration': 240.0, 'frequency': 659.2},
                              {'duration': 240.0, 'frequency': 830.6},
                              {'duration': 240.0, 'frequency': 1108.8},
                              {'duration': 480.0, 'frequency': 880.0},
                              {'duration': 480.0, 'frequency': 0},
                              {'duration': 240.0, 'frequency': 740.0},
                              {'duration': 240.0, 'frequency': 622.2},
                              {'duration': 240.0, 'frequency': 740.0},
                              {'duration': 240.0, 'frequency': 987.8},
                              {'duration': 480.0, 'frequency': 830.6},
                              {'duration': 240.0, 'frequency': 740.0},
                              {'duration': 240.0, 'frequency': 659.2},
                              {'duration': 480.0, 'frequency': 0},
                              {'duration': 240.0, 'frequency': 659.2},
                              {'duration': 240.0, 'frequency': 554.4},
                              {'duration': 480.0, 'frequency': 740.0},
                              {'duration': 480.0, 'frequency': 554.4},
                              {'duration': 480.0, 'frequency': 0},
                              {'duration': 240.0, 'frequency': 740.0},
                              {'duration': 240.0, 'frequency': 659.2},
                              {'duration': 480.0, 'frequency': 830.6},
                              {'duration': 480.0, 'frequency': 740.0}]}
        self.assertDictEqual(parse_rtttl(barbie_girl_with_whitespaces), expected)

    def test_parsing_rtttl_with_non_strict_note_syntax(self):
        rtttl = 'Test:d=4,o=5,b=90:F#6.,8F#.6,f#'

        expected = {'title': 'Test',
                    'notes': [{'duration': 1000.0, 'frequency': 1480.0},
                              {'duration': 500.0, 'frequency': 1480.0},
                              {'duration': 666.667, 'frequency': 740.0}]}

    def test_parsing_rtttl_with_strict_note_syntax(self):
        valid_rtttl = 'Valid:d=4,o=5,b=90:F#6.,8F#6.,f#'
        invalid_rtttl = 'Invalid:d=4,o=5,b=90:F#6.,8F#.6,f#'

        expected = {'title': 'Valid',
                    'notes': [{'duration': 1000.0, 'frequency': 1480.0},
                              {'duration': 500.0, 'frequency': 1480.0},
                              {'duration': 666.667, 'frequency': 740.0}]}

        self.assertDictEqual(parse_rtttl(valid_rtttl, strict_note_syntax=True), expected)
        self.assertRaises(InvalidNote, parse_rtttl, invalid_rtttl, True)

    def test_parsing_invalid_rtttl(self):
        cases = [
            'title;d=8,o=5,b=125;g#,e,g',
            'title;g#,e,g',
            'title:d=8,o=5,b=125:g#,e,g:foo',
        ]

        for case in cases:
            self.assertRaises(InvalidRTTTLFormat, parse_rtttl, case)

if __name__ == 'main':
    unittest.main()

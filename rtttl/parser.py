import re
from rtttl.exceptions import InvalidNote

def remove_whitespaces(string):
    return ''.join(string.split())

def correct_note_syntax(note):
    return re.sub(r'^(\d*)([pbeh]|[cdfga]#?)(\.?)(\d*)$', r'\1\2\4\3', note)

def parse_note(note_str):
    try:
        elements = re.findall(r'^(\d{0,2})([pbeh]|[cdfga]#?)(\d?)(\.?)$', note_str)[0]
    except:
        raise InvalidNote()

    funcs = (parse_duration, parse_pitch, parse_octave, has_dot)
    elements = [func(element) for func, element in zip(funcs, elements)]
    keys = ('duration', 'pitch', 'octave', 'dot')
    return dict(zip(keys, elements))

def parse_duration(duration):
    allowed_duration = [1, 2, 4, 8, 16, 32]
    return parse_int(duration, allowed_duration)

def parse_octave(octave):
    allowed_octave = [4, 5, 6, 7]
    return parse_int(octave, allowed_octave)

def parse_pitch(pitch):
    allowed_pitch = ['p', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'h', 'b']
    return parse_element(pitch, allowed_pitch)

def parse_int(element, allowed) :
    if element:
        return parse_element(int(element), allowed)
    return None

def parse_element(element, allowed):
    if element in allowed:
        return element
    else:
        raise InvalidNote()

def has_dot(dot):
    return dot == '.'

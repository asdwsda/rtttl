import re

def remove_whitespaces(string):
    return ''.join(string.split())

def correct_note_syntax(note):
    return re.sub(r'^(\d*)([pbeh]|[cdfga]#?)(\.?)(\d*)$', r'\1\2\4\3', note)

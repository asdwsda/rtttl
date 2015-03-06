# RTTTL
Ring Tone Text Transfer Language (RTTTL) parser for python

## Usage
```python
>>> import pprint
>>> from rtttl import parse_rtttl

>>> barbie = parse_rtttl('Barbie girl:d=4,o=5,b=125:8g#,8e,8g#,8c#6,a,p,8f#,8d#,8f#,8b,g#,8f#,8e,p,8e,8c#,f#,c#,p,8f#,8e,g#,f#')

>>> pprint.pprint(barbie)
{'notes': [{'duration': 240.0, 'frequency': 830.6},
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
           {'duration': 480.0, 'frequency': 740.0}],
 'title': 'Barbie girl'}
```

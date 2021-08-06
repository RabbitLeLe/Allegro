#-*- coding: utf-8 -*-
import re

def clear_tel(tel):
    y = {
        ' ': '',
        '+48': '',
        '(+48)': '',
        '-': '',
        '.': '',
        ',': '',
        '*': '',
        '_': '',
        '.': '',
        ',': '',
        ')': '',
        '(': ''
        }
    for i, j in y.items():
        tel = tel.replace(i, j)
    return tel

def clear_text(text):
    x = {
    'ę': 'e',
    'Ę': 'e',
    'ó': 'o',
    'Ó': 'o',
    'ą': 'a',
    'Ą': 'a',
    'ś': 's',
    'Ś': 's',
    'ł': 'l',
    'Ł': 'l',
    'ż': 'z',
    'Ż': 'z',
    'ź': 'z',
    'Ź': 'z',
    'ć': 'c',
    'Ć': 'c',
    'ń': 'n',
    'Ń': 'n',
    '\n': '',
    '\t': '',
    '\r': '',
    "'": '"',
    ';': ':',
    '²': '2',
    '<p>': '',
    '</p>': '',
    '<br>': '',
    '<br/>': '',
    '<br />': '',
    '<strong>': '',
    '</strong>': '',
    '<li>': '',
    '</li>': '',
    '<ul>': '',
    '</ul>': '',
    '<em>': '',
    '</em>': '',
    '<u>': '',
    '</u>': ''
            }
    for i, j in x.items():
        text = text.replace(i, j)
    multi_spaces = re.compile(r"\s+")
    text = multi_spaces.sub(" ", text).strip()
    return text
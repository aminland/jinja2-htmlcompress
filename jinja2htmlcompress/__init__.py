#!/usr/bin/env python
# coding=utf-8
"""
    jinja2htmlcompress
    ~~~~~~~~~~~~~~~~~~

    A Jinja2 extension that eliminates useless whitespace at template
    compilation time without extra overhead.

    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import re
from jinja2.ext import Extension
from jinja2.lexer import Token, describe_token
from jinja2 import TemplateSyntaxError

_tag_re = re.compile(r'<(/?)([a-zA-Z0-9_-]+)|(\s*>)', re.S)
_ws_normalize_re = re.compile(r'[ \t\r\n]+')
_ws_linewrap_re = re.compile(r'^\s*\n\s*|\s*\n\s*$')

class CompressError(Exception):
    def __init__(self, message):
        self.message = message

def _make_dict_from_listing(listing):
    rv = {}
    for keys, value in listing:
        for key in keys:
            rv[key] = value
    return rv

class Compressor:
    isolated_elements = set(['script', 'style', 'noscript', 'textarea', 'pre'])
    void_elements = set([
        'br', 'img', 'area', 'hr', 'param', 'input', 'embed', 'col',
        'meta', 'link',
    ])
    block_elements = set([
        'div', 'p', 'form', 'ul', 'ol', 'li', 'table', 'tr',
        'tbody', 'thead', 'tfoot', 'tr', 'td', 'th', 'dl',
        'dt', 'dd', 'blockquote', 'h1', 'h2', 'h3', 'h4',
        'h5', 'h6',
    ])
    breaking_rules = _make_dict_from_listing([
        (['p'], set(['#block'])),
        (['li'], set(['li'])),
        (['td', 'th'], set(['td', 'th', 'tr', 'tbody', 'thead', 'tfoot'])),
        (['tr'], set(['tr', 'tbody', 'thead', 'tfoot'])),
        (['thead', 'tbody', 'tfoot'], set(['thead', 'tbody', 'tfoot'])),
        (['dd', 'dt'], set(['dl', 'dt', 'dd']))
    ])
    def __init__(self):
        self.stack = []

    def is_isolated(self, stack):
        for tag in reversed(stack):
            if tag in self.isolated_elements:
                return True
        return False

    def is_breaking(self, tag, other_tag):
        breaking = self.breaking_rules.get(other_tag)
        return breaking and (tag in breaking or
            ('#block' in breaking and tag in self.block_elements))

    def enter_tag(self, tag):
        while self.stack and self.is_breaking(tag, self.stack[-1]):
            self.leave_tag(self.stack[-1])
        if tag not in self.void_elements:
            self.stack.append(tag)

    def leave_tag(self, tag):
        if not self.stack:
            raise CompressError('Tried to leave "%s" but something closed '
                     'it already' % tag)
        if tag == self.stack[-1]:
            self.stack.pop()
            return
        for idx, other_tag in enumerate(reversed(self.stack)):
            if other_tag == tag:
                for num in range(idx + 1):
                    self.stack.pop()
            elif not self.breaking_rules.get(other_tag):
                break

    def compress(self, value):
        def normalize(value, keep_linewrap = True):
            if not self.is_isolated(self.stack):
                value = _ws_linewrap_re.sub(' ' if keep_linewrap else '', value)
                value = _ws_normalize_re.sub(' ', value)
            return value
        pos = 0
        buf = []
        for match in _tag_re.finditer(value):
            closes, tag, sole = match.groups()
            preamble = value[pos : match.start()]
            if sole:
                preamble = preamble.rstrip()
                preamble = _ws_normalize_re.sub(' ', preamble)
            else:
                preamble = normalize(preamble, pos == 0)
            buf.append(preamble)
            if sole:
                buf.append(sole.strip())
            else:
                buf.append(match.group())
                (self.leave_tag if closes else self.enter_tag)(tag)
            pos = match.end()

        buf.append(normalize(value[pos:], pos > 0))
        return u''.join(buf)

class HTMLCompress(Extension):
    def fail(self, message, stream, token):
        raise TemplateSyntaxError(message, token.lineno,
                stream.name, stream.filename)

    def filter_stream(self, stream):
        compressor = Compressor()
        for token in stream:
            if token.type != 'data':
                yield token
                continue
            try:
                value = compressor.compress(token.value)
            except CompressError as e:
                self.fail(e.message, stream, token)
            else:
                yield Token(token.lineno, 'data', value)


class SelectiveHTMLCompress(HTMLCompress):
    def filter_stream(self, stream):
        compressor = Compressor()
        strip_depth = 0
        while 1:
            if stream.current.type == 'block_begin':
                if stream.look().test('name:strip') or \
                   stream.look().test('name:endstrip'):
                    stream.skip()
                    if stream.current.value == 'strip':
                        strip_depth += 1
                    else:
                        strip_depth -= 1
                        if strip_depth < 0:
                            self.fail('Unexpected tag endstrip', stream, token)
                    stream.skip()
                    if stream.current.type != 'block_end':
                        self.fail('expected end of block, got %s' %
                                 describe_token(stream.current), stream, token)
                    stream.skip()
            if strip_depth > 0 and stream.current.type == 'data':
                token = stream.current
                try:
                    value = compressor.compress(token.value)
                except CompressError as e:
                    self.fail(e.message, stream, token)
                else:
                    yield Token(stream.current.lineno, 'data', value)
            else:
                yield stream.current
            next(stream)

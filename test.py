#!/usr/bin/env python
# coding=utf-8
from jinja2 import Environment
from jinja2htmlcompress import HTMLCompress, SelectiveHTMLCompress

def test():
    env = Environment(extensions=[HTMLCompress])
    tmpl = env.from_string('''
        <html>
          <head>
            <title>{{ title }}</title>
          </head>
          <script type=text/javascript>
            if (foo < 42) {
              document.write('Foo < Bar');
            }
          </script>
          <body >
            <li><a href="{{ href }}">{{ title }}</a><br>Test   Foo
            <li><a href="{{ href }}">{{ title }}</a><img src=test.png>
            <li{% if True %} class="active"{% endif %} >Active item</li>
            <p>
                This page has been moved <a href="{{url}}">here</a>
                {{- ' permenantly' if status == 301 else '' -}}
                .
            </p>
          </body >
        </html>
    ''')
    print(tmpl.render(title=42, href='index.html'))

    env = Environment(extensions=[SelectiveHTMLCompress])
    tmpl = env.from_string('''
        Normal   <span>  unchanged </span> stuff
        {% strip %}Stripped <span class=foo   id=bar  >   test   </span>
        <a href="foo">  test </a> {{ foo }}
        Normal <stuff>   again {{ foo }}  </stuff>
        <p>
          Foo<br>Bar
          Baz
        <p>
          Moep    <span>Test</span>    Moep
        </p>
        {% endstrip %}
    ''')
    print(tmpl.render(foo=42))

test()

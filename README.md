jinja2-htmlcompress
===

A Jinja2 extension that removes whitespace between HTML tags.

Installation
---
``` sh
$ pip3 install git+https://github.com/gera2ld/jinja2-htmlcompress.git
```

Usage
---
``` python
env = Environment(extensions=['jinja2htmlcompress.HTMLCompress'])
```

How does it work?  It throws away all whitespace between HTML tags
it can find at runtime.  It will however preserve pre, textarea, style
and script tags because this kinda makes sense.  In order to force
whitespace you can use `{{ " " }}`.

Unlike filters that work at template runtime, this remotes whitespace
at compile time and does not add an overhead in template execution.

What if you only want to selective strip stuff?

``` python
env = Environment(extensions=['jinja2htmlcompress.SelectiveHTMLCompress'])
```

And then mark blocks with `{% strip %}`:

``` html
{% strip %} ... {% endstrip %}
```

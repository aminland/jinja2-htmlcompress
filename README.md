jinja2-htmlcompress
===

A Jinja2 extension that removes whitespace between HTML tags.

Installation
---
``` sh
$ pip3 install git+https://github.com/gera2ld/jinja2-htmlcompress.git
```

Why this?
---
[mitsuhiko's jinja2-htmlcompress](https://github.com/mitsuhiko/jinja2-htmlcompress)
will strip white spaces between tokens and splitted text, which breaks cases below:
``` html
<li{% if active %} class="active"{% endif %}>Active item</li>
<!-- output
<liclass="active">Active item</li>
-->
```
This fork will keep one space at the start and end for each of the splitted pieces.

Usage
---
* Compress all HTML

  ``` python
  env = Environment(extensions=['jinja2htmlcompress.HTMLCompress'])
  ```

* Compress partial HTML

  ``` python
  env = Environment(extensions=['jinja2htmlcompress.SelectiveHTMLCompress'])
  ```

  And then mark blocks with `{% strip %}`:

  ``` html
  {% strip %} ... {% endstrip %}
  ```

* How does it work?

  It throws away all whitespace between HTML tags it can find at runtime.
  It will however preserve pre, textarea, style and script tags because
  this kinda makes sense. In order to force whitespace you can use
  `{{ " " }}`.

  Unlike filters that work at template runtime, this remotes whitespace
  at compile time and does not add an overhead in template execution.

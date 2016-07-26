jinja2-htmlcompress
===

A Jinja2 extension that removes whitespace between HTML tags.

Based on [mitsuhiko's jinja2-htmlcompress](https://github.com/mitsuhiko/jinja2-htmlcompress).

Installation
---
``` sh
$ pip3 install git+https://github.com/gera2ld/jinja2-htmlcompress.git
```

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

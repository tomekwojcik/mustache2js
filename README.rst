mustache2js
~~~~~~~~~~~

Awesome Mustache to JavaScript converter.

This script wraps Mustache templates in some JavaScript to make using Mustache
templates in Web apps easier. The wrapping is done using CoffeeScript.

Usage
-----

``mustache2js [options] file1 file2 file...``

For list of options see ``mustache2js -h``

WTF?
----

Hack your template, convert it to JavaScript string and wrap the string in some
code to make it available to the browser.

The code that does the wrapping is::
    
    window.templates["{template_name}"] = """{template}"""
    
where ``template_name`` is the file name and ``template`` is, well, the template
itself :).

This is CoffeeScript code that's then compiled to JavaScript with ``coffee``.
Make sure you have CoffeeScript compiler in your path.

You can change the wrapping code using ``-t`` option.

License
-------

MIT-style, see LICENSE.
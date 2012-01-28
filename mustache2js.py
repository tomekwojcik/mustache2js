#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012 Tomek Wójcik <labs@tomekwojcik.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
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

The code that does the wrapping is stored in ``TEMPLATE``, where 
``template_name`` is the file name and ``template`` is, well, the template
itself :).

This is CoffeeScript code that's then compiled to JavaScript with ``coffee``.
Make sure you have CoffeeScript compiler in your path.

You can change the wrapping code using ``-t`` option.
"""

import sys
import optparse
import subprocess
import os
import time

TEMPLATE = u'window.templates["{template_name}"] = """{template}"""'

def locate_coffee():
    """
    Determine and return ``coffee`` binary path or ``None``.
    """
    proc = subprocess.Popen([ 'which', 'coffee' ], stdout=subprocess.PIPE)
    return_code = proc.wait()
    
    if return_code != 0:
        return None
        
    coffee_path = proc.stdout.read().strip()
    
    return coffee_path
        
def main():
    """
    Do Teh Magic.
    """
    progname = sys.argv[0]
    usage = 'usage: %prog [options] file1 file2 file...'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-d', '--destdir', metavar='DESTDIR', dest='destdir', default='.', help='store output files in DESTDIR [default: %default]')
    parser.add_option('-t', '--template', metavar='TEMPLATE', dest='template', default=None, help='use Mustache TEMPLATE to generate CoffeeScript files'),
    parser.add_option('-w', '--watch', action='store_true', dest='watch', default=False, help='watch files for changes')
    
    (options, args) = parser.parse_args()
        
    if len(args) == 0:
        parser.print_help()
        sys.exit(64)
        
    template = TEMPLATE
    if options.template != None:
        _template_file = file(options.template, 'r')
        template = _template_file.read().decode('utf-8')
        _template_file.close()
        
    coffee_path = locate_coffee()
    if coffee_path == None:
        print '%s: coffee not found' % (progname, )
        sys.exit(1)
        
    def convert_file(path):
        """
        Compile Mustache template in ``path`` to JS.
        """
        print 'Converting "%s"...' % (path, )
        source_file = file(path, 'r')
        source = source_file.read().decode('utf-8')
        source_file.close()
        
        template_name = os.path.splitext(os.path.basename(path))[0]
        coffee_code = template.format(template_name=template_name, template=source)
        
        proc = subprocess.Popen([ coffee_path, '-b', '-c', '-s' ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        compiled, proc_err = proc.communicate(input=coffee_code)
        
        if proc.returncode != 0:
            print proc_err
            sys.exit(1)
        
        dest_filename = os.path.join(options.destdir, template_name + '.js')
        dest_file = file(dest_filename, 'w')
        dest_file.write(compiled.encode('utf-8'))
        dest_file.close()

    mtimes = {}
    while True:
        for template_file in args:
            try:
                mtime = os.path.getmtime(template_file)
            except os.error:
                print '%s: no such file or directory: %s' % (sys.argv[0], template_file)
                
            if mtimes.has_key(template_file) == False or mtimes[template_file] != mtime:
                convert_file(template_file)
                mtimes[template_file] = mtime
            
        if options.watch == False:
            break
            
        time.sleep(1)
    
if __name__ in ('main', '__main__'):
    main()
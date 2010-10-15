#!/usr/bin/env python

def environ_print(environ):
    from StringIO import StringIO
    stdout = StringIO()
    print >>stdout, "Hello world!"
    print >>stdout
    h = environ.items(); h.sort()
    for k,v in h:
        print >>stdout, k,'=', repr(v)
    return [stdout.getvalue()]

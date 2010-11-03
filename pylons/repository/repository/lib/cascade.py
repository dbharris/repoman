class Cascade(object):
    """
    Modified version of paste.cascade.Cascade
        based off: Paste-1.7.5.1-py2.4
    """

    def __call__(self, environ, start_response):
        """

        """
        failed = []
        def repl_start_response(status, headers, exc_info=None):
            code = int(status.split(None, 1)[0])
            if code in self.catch_codes:
                failed.append(None)
                return _consuming_writer
            return start_response(status, headers, exc_info

        try:
            length = int(environ.get('CONTENT_LENGTH', 0) or 0)
        except ValueError:
            length = 0
        if length > 0:
            # We have to copy wsgi.input
            copy_wsgi_input = True
            if length > 4096 or length < 0:
                f = tempfile.TemporaryFile()
                if length < 0:
                    f.write(environ['wsgi.input'].read())
                else:
                    copy_len = length
                    while copy_len > 0:
                        chunk = environ['wsgi.input'].read(min(copy_len, 4096))
                        if not chunk:
                            raise IOError("Request body truncated")
                        f.write(chunk)
                        copy_len -= len(chunk)
                f.seek(0)
            else:
                f = StringIO(environ['wsgi.input'].read(length))
            environ['wsgi.input'] = f
        else:
            copy_wsgi_input = False
        for app in self.apps[:-1]:
            environ_copy = environ.copy()
            if copy_wsgi_input:
                environ_copy['wsgi.input'].seek(0)
            failed = []
            try:
                v = app(environ_copy, repl_start_response)
                if not failed:
                    return v
                else:
                    if hasattr(v, 'close'):
                        # Exhaust the iterator first:
                        list(v)
                        # then close:
                        v.close()
            except self.catch_exceptions, e:
                pass
        if copy_wsgi_input:
            environ['wsgi.input'].seek(0)
        return self.apps[-1](environ, start_response)


"""
Vercel Serverless Function entry point for Flask.
Exposes the WSGI application instance wrapped with a middleware
that restores the original request path from Vercel's rewrite query parameter.
"""

import os
import sys
import urllib.parse

# Ensure root directory is in Python path for absolute imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app


class VercelRewriteMiddleware:
    """
    Restores the real URL path requested by the client from Vercel's rewrite (__path=/$1).
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = environ.get('QUERY_STRING', '')
        if qs:
            params = urllib.parse.parse_qs(qs, keep_blank_values=True)
            if '__path' in params:
                path_val = params.pop('__path')[0]
                if not path_val.startswith('/'):
                    path_val = '/' + path_val
                environ['PATH_INFO'] = path_val
                environ['QUERY_STRING'] = urllib.parse.urlencode(params, doseq=True)

        return self.wsgi_app(environ, start_response)


# Wrap Flask's WSGI callable with path normalizer
app.wsgi_app = VercelRewriteMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run()

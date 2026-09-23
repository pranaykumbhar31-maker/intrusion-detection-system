"""
Vercel Serverless Function entry point for Flask.
Exposes the WSGI application instance wrapped with a middleware
that normalizes Vercel's rewritten paths (x-matched-path / /api/index).
"""

import os
import sys

# Ensure root directory is in Python path for absolute imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app


class VercelPathMiddleware:
    """
    Middleware that fixes path routing on Vercel:
    1. If Vercel passed the original URL in HTTP_X_MATCHED_PATH, use that.
    2. If PATH_INFO starts with /api/index, strip it so Flask matches root routes.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        matched_path = environ.get('HTTP_X_MATCHED_PATH')
        if matched_path:
            environ['PATH_INFO'] = matched_path
        else:
            path_info = environ.get('PATH_INFO', '')
            for prefix in ['/api/index.py', '/api/index']:
                if path_info.startswith(prefix):
                    remainder = path_info[len(prefix):]
                    environ['PATH_INFO'] = remainder if (remainder and remainder.startswith('/')) else ('/' + remainder.lstrip('/'))
                    break

        return self.wsgi_app(environ, start_response)


# Wrap Flask's WSGI callable with path normalizer
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run()

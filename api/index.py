"""
Vercel Serverless Function entry point.
Exposes the Flask WSGI application instance for Vercel Python runtime.
"""

import os
import sys

# Add project root directory to sys.path so modules like predict.py and templates are found
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app

# Vercel looks for the WSGI application variable named 'app'
if __name__ == '__main__':
    app.run()

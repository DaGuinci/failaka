#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Add application directory to Python path
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, script_dir)

# Add embedded dependencies if they exist
vendor_dir = os.path.join(script_dir, 'vendor')
if os.path.exists(vendor_dir):
    sys.path.insert(0, vendor_dir)

import django
from django.core.wsgi import get_wsgi_application

# Define Django configuration module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'failaka.settings')

# Initialiser Django
django.setup()

# Obtenir l'application WSGI
application = get_wsgi_application()

# Interface CGI
if __name__ == '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(application)
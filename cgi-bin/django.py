#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Ajouter le répertoire de l'application au Python path
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, script_dir)

# Ajouter les dépendances embarquées si elles existent
vendor_dir = os.path.join(script_dir, 'vendor')
if os.path.exists(vendor_dir):
    sys.path.insert(0, vendor_dir)

import django
from django.core.wsgi import get_wsgi_application

# Définir le module de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'failaka.settings')

# Initialiser Django
django.setup()

# Obtenir l'application WSGI
application = get_wsgi_application()

# Interface CGI
if __name__ == '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(application)
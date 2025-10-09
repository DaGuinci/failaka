#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Ajouter le répertoire de l'application au Python path
sys.path.insert(0, '/home/gufo9311/www')

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
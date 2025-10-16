#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Content-Type: text/html\n")
print("<h1>O2switch Django Debug</h1>")

try:
    import sys
    import os
    print(f"<p>Python version: {sys.version}</p>")
    
    # Test application directory
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"<p>App directory: {script_dir}</p>")
    print(f"<p>Files in app dir: {os.listdir(script_dir)[:10]}</p>")
    
    # Add paths like in django.py
    sys.path.insert(0, script_dir)
    vendor_dir = os.path.join(script_dir, 'vendor')
    if os.path.exists(vendor_dir):
        sys.path.insert(0, vendor_dir)
        print(f"<p>✅ Vendor directory found</p>")
    else:
        print(f"<p>⚠️ No vendor directory</p>")
    
    # Test d'import Django
    try:
        import django
        print(f"<p>✅ Django found: {django.VERSION}</p>")
        
        # Test des settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'failaka.settings')
        print(f"<p>✅ Settings module set</p>")
        
        # Test setup Django
        django.setup()
        print(f"<p>✅ Django setup OK</p>")
        
        # Test WSGI
        from django.core.wsgi import get_wsgi_application
        app = get_wsgi_application()
        print(f"<p>✅ WSGI application created: {type(app)}</p>")
        
    except Exception as django_error:
        print(f"<p>❌ Django error: {django_error}</p>")
        import traceback
        print(f"<pre>{traceback.format_exc()}</pre>")
        
except Exception as e:
    print(f"<p>❌ General error: {e}</p>")
    import traceback
    print(f"<pre>{traceback.format_exc()}</pre>")
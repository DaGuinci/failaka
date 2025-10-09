#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Content-Type: text/html\n")
print("<h1>O2switch Python Environment</h1>")

try:
    import sys
    print(f"<p>Python version: {sys.version}</p>")
    print(f"<p>Python path: {sys.path[:5]}</p>")
    
    # Test des modules disponibles
    modules_to_test = ['django', 'sqlite3', 'os', 'json', 'urllib']
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"<p>✅ {module} available</p>")
        except ImportError:
            print(f"<p>❌ {module} NOT available</p>")
    
    # Liste des modules installés
    print("<h2>Installed packages:</h2>")
    try:
        import pkg_resources
        installed = [d.project_name for d in pkg_resources.working_set]
        print(f"<p>Found {len(installed)} packages</p>")
        for pkg in sorted(installed)[:20]:  # Premiers 20
            print(f"<p>• {pkg}</p>")
    except:
        print("<p>Cannot list packages</p>")
        
except Exception as e:
    print(f"<p>❌ Error: {e}</p>")
    import traceback
    print(f"<pre>{traceback.format_exc()}</pre>")
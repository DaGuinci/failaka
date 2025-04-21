# failaka
Sauvegarde et valorisation des archives de la mission Failaka

https://failalka.readthedocs.io/en/latest/

## Useful commands


To launch the server:
```bash
    python manage.py runserver
```

To launch tests suite:
```bash
    python manage.py test
```

To reboot the database (DELETE ALL DATAS):
```bash
    python manage.py flush
    python manage.py loaddata initial_data.json
```
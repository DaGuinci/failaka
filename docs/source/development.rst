===========
Development
===========

Context
-------

Backup and Enhancement of the Failalka Mission items.

Inspired by [this website](https://desertnetworks.huma-num.fr/)

Local installation
------------------

1. Prerequisites

Have a database installed on your machine (PostgreSQL, MySQL, SQLite, etc.)

2. Clone git repertory

.. code-block:: bash

    git clone https://github.com/DaGuinci/failalka.git

3. Virtual environment creation

.. code-block:: bash

    cd Orange-County-Lettings
    python -m venv env

* Activate

.. code-block:: bash

    source env/bin/activate

4. Install dependencies

.. code-block:: bash

    pip install -r requirements.txt

5. Create a `.env` file at the root of the project with the following content:

.. code-block:: bash

    DJANGO_ENV='development'
    SECRET='your_secret_key'
    DJANGO_SUPERUSER_USERNAME='superadmin'
    DJANGO_SUPERUSER_PASSWORD='superadmin'
    DJANGO_SUPERUSER_EMAIL='your_email'

6. Run the migrations

.. code-block:: bash

    python manage.py migrate

7. Run the server

.. code-block:: bash

    python manage.py runserver

8. Open your browser and go to the following address:

``http://localhost:8000``


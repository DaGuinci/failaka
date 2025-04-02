============
Installation
============

Contexte
--------

Orange County Lettings est une start-up dans le secteur de la
location de biens immobiliers.

La start-up est en pleine phase d’expansion aux États-Unis.

La présente documentation concerne le développement du site web de cette start-up,
disponible à `cette adresse <https://oc-orange-county-letting.onrender.com/>`_.

Installation du site en local
-----------------------------

1. Cloner le repertoire git

.. code-block:: bash

    cd /emplacement/du/dossier/contenant/le/projet
    git clone https://github.com/DaGuinci/Orange-County-Lettings.git

2. Créer l'environnement virtuel

.. code-block:: bash

    cd Orange-County-Lettings
    python -m venv venv

* Activer l'environnement

.. code-block:: bash

    source venv/bin/activate


* Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel

.. code-block:: bash

    which python


* Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure

.. code-block:: bash

    python --version


* Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel

.. code-block:: bash

    which pip


* Pour désactiver l'environnement (à titre indicatif)

.. code-block:: bash

    deactivate


3. Exécuter le site

.. code-block:: bash

    cd /path/to/Python-OC-Lettings-FR
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py runserver

* Aller sur `http://localhost:8000` dans un navigateur.

Administration
--------------

Se rendre sur le panel d'administration:

* en local, ``http://localhost:8000/admin``

* Sur le site déployé,
  ``https://oc-orange-county-letting.onrender.com/admin``

Se connecter avec l'utilisateur `admin` et le mot de passe `Abc1234!`
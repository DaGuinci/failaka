Proposer une modification
=========================

Cas d'usage
-----------

On souhaite par exemple modifier le titre du site.

Actuellement "Welcome to Holiday Homes", on souhaite un nouveau titre:
"Welcome to the Orange County Lettings Website"

Procédure
---------

1. Travail en local

    **Prérequis**

    Avant de pouvoir effectuer une modification il est nécessaire d'
    :ref:`installer le site en local <installation du site en local>`.

    Pour accéder au projet sur CircleCi, tester les images du Docker Hub
    ou visualiser les erreurs sur Sentry, contacter l'administrateur
    à l'adresse `daguinci@mailo.com <daguinci@mailo.com>`_.

    * Dans un terminal, se rendre à la racine du projet et activer l'environnement

    .. code-block:: python

        cd emplacement/du/projet
        source venv/bin/activate

    * S'assurer d'avoir la dernière version dev à jour:

    .. code-block:: bash

        git checkout dev
        git fetch

    * Créer une nouvelle branche

    .. code-block:: bash

        git checkout -b content/change-title

    *L'option -b permet de basculer instantanément sur la nouvele branche*

    * Effectuer la modification

    Dans notre cas, on modifie le fichier ./home/templates/home/index.html,
    à la ligne 10:

    .. code-block:: html

        <h1 class="page-header-ui-title mb-3 display-6">Welcome to the Orange County Lettings Website</h1>

    * Tester la modification en local

    .. code-block:: bash

        python manage.py runserver

    Puis se rendre sur `http://localhost:8000` à l'aide d'un navigateur.

    * Vérifier qu'aucune fonction du site n'a été impactée par la modification

    .. code-block:: bash

        pytest --cov=.

    .. note::

        La suite de tests intègre la génération d'une erreur 500.
        En cas d'activation de Sentry, une erreur
        est envoyée à chaque execution des tests.

    * Activer le logging sur Sentry

    Ajouter en local un fichier .env à la racine du projet:

    .. code-block:: python

        # .env

        SENTRY_KEY=<clé sentry>

    Puis accéder au rapport d'erreur sur Sentry.

    Si tous les tests passent, on passe à l'étape suivante.

    * Créer une image en local pour test

    .. code-block:: bash

        docker build -t daguinci/oc-letting:<nom-de-votre-commit> .
        docker run -it --rm -p 8000:8000 daguinci/oc-letting:<nom-de-votre-commit>

    On peut à présent aller sur `http://localhost:8000` à l'aide d'un navigateur.

    .. warning::

        Attention à bien mentionner le nom du commit, sous peine d'écraser
        latest, la dernière image stable, en cas de push.

    * Maintenir le respect des normes pep8

    .. code-block:: bash

        flake8

    Le cas échéant, effectuer les corrections pour
    n'avoir aucune erreur flake8.

    * Effectuer un commit de la modification

    .. code-block:: bash

        git add .
        git commit -m "content(index.html): site's title modification"

    * Mettre à jour la documentation

    Bien que ce ne soit pas nécessaire dans notre cas d'usage,
    c'est ce moment qu'on préférera pour modifier la documentation.

    Pour cela on modifiera l'un des fichiers .rst présents dans ./docs/source,
    voire le fichier .docs/index.rst en cas de nouvelle section, pour la faire
    apparaître dans le sommaire.

    .. note::
        Le diagramme entité-relation de la base de données est généré
        avec `draw.io <https://www.drawio.com/>`_, puis exporté sous ERD.svg.
        Les documents ./docs/source/entity_relation_diagram.drawio et
        ./docs/source/ERD.svg devront donc être modifié en cas de changement de
        la structure de la base de données.

    * Tester la documentation en local

    .. code-block:: bash

        cd docs
        make html

    Afficher la nouvelle documentation en ouvrant le fichier
    .docs/_build/html/index.html

    * Faire un commit de la documentation

    .. code-block:: bash

        git add .
        git commit -m "docs(fichier.rst): upd doc for this feature or fix"


2. Pousser les modifications sur dev

    * Merger sur dev

    .. code-block:: bash

        git checkout dev
        git fetch
        git merge content/change-title

    * Pousser sur le dépôt Github

    .. code-block:: bash

        git push origin dev

    * Tester l'image ainsi buildée

    Après quelques minutes, une nouvelle image docker a été envoyée sur Docker Hub lors
    de l'envoi d'un commit sur dev.

    .. code-block:: python

        docker run -it --rm --pull=always -p 8000:8000 daguinci/oc-letting

    Aller sur `http://localhost:8000` à l'aide d'un navigateur.

    * Vérifier que les tests sont passés sur la pipeline de CircleCi

    * Vérifier la mise à jour de la documentation sur https://daguinci-orange-county-lettings.readthedocs.io/fr/dev/

3. Déployer le site

    Le déploiement se réalise automatiquement à travers CircleCi,
    en cas de commit sur la branche master.

    .. code-block:: bash

        git checkout master
        git merge dev
        git push origin master

    * Vérifier le processus de déploiement sur CircleCi

    * Vérfifier la mise à jour de la documentation sur https://daguinci-orange-county-lettings.readthedocs.io/fr/latest/

    * Vérifier la modification en ligne sur https://oc-orange-county-letting.onrender.com/


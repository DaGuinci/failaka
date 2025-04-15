import requests
from django.shortcuts import render

# def fetch_name(api_url, uuid):
#     """Effectue une requête pour récupérer le nom associé à un UUID."""
#     try:
#         response = requests.get(f"{api_url}/{uuid}/")
#         response.raise_for_status()
#         data = response.json()
#         return data.get('name', 'Nom inconnu')  # Retourne le nom ou 'Nom inconnu' si absent
    
#     except requests.exceptions.RequestException as e:
#         print(f"Erreur lors de la récupération du nom pour {uuid} : {e}")
#         return 'Nom inconnu'

def home(request):
    # URL de l'API pour récupérer les items
    base_api_url = request.build_absolute_uri('/api/')
    
    try:
        # Effectuer une requête GET à l'API
        response = requests.get(base_api_url + 'items/')
        response.raise_for_status()  # Vérifie les erreurs HTTP
        data = response.json()  # Convertit la réponse en JSON
        items = data.get('results', [])  # Récupère la liste des items

    except requests.exceptions.RequestException as e:
        # En cas d'erreur, afficher un message d'erreur
        items = []
        print(f"Erreur lors de la récupération des items : {e}")

    # Rendre le template avec les items
    return render(request, 'client/home.html', {'items': items})
import requests
from django.shortcuts import render


def home(request):
    # API URL to retrieve items
    base_api_url = request.build_absolute_uri('/api/')
    
    try:
        # Make a GET request to the API
        response = requests.get(base_api_url + 'items/')
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()  # Convert the response to JSON
        items = data.get('results', [])  # Retrieve the list of items

    except requests.exceptions.RequestException as e:
        # In case of an error, display an error message
        items = []
        print(f"Error while retrieving items: {e}")

    # Render the template with the items
    return render(request, 'client/home.html', {'items': items})

def item_detail(request, item_id):
    # API URL to retrieve item details
    base_api_url = request.build_absolute_uri('/api/')
    
    try:
        # Make a GET request to the API
        response = requests.get(base_api_url + f'items/{item_id}/')
        response.raise_for_status()  # Check for HTTP errors
        item = response.json()  # Convert the response to JSON

    except requests.exceptions.RequestException as e:
        # In case of an error, display an error message
        item = {}
        print(f"Error while retrieving item {item_id}: {e}")

    # Render the template with the item details
    return render(request, 'client/item_detail.html', {'item': item})
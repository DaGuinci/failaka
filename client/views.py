import requests
from django.shortcuts import render

def items_list(request):
    # API URL to retrieve items
    base_api_url = request.build_absolute_uri('/api/')
    items = []

    try:
        # Initial URL for the first page
        url = base_api_url + 'items/'
        while url:
            # Make a GET request to the API
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()  # Convert the response to JSON
            items.extend(data.get('results', []))  # Append the results to the items list
            url = data.get('next')  # Get the URL for the next page

    except requests.exceptions.RequestException as e:
        # In case of an error, display an error message
        print(f"Error while retrieving items: {e}")

    # Render the template with the items
    return render(request, 'client/home.html', {'items': items})

def item_detail(request, item_uuid):
    # API URL to retrieve item details
    base_api_url = request.build_absolute_uri('/api/')
    
    try:
        # Make a GET request to the API
        response = requests.get(base_api_url + f'items/{item_uuid}/')
        response.raise_for_status()  # Check for HTTP errors
        item = response.json()  # Convert the response to JSON

    except requests.exceptions.RequestException as e:
        # In case of an error, display an error message
        item = {}
        print(f"Error while retrieving item {item_uuid}: {e}")

    # Render the template with the item details
    return render(request, 'client/item_detail.html', {'item': item})

def site_detail(request, site_uuid):
    # API URL to retrieve site details
    base_api_url = request.build_absolute_uri('/api/')
    print(base_api_url)
    
    try:
        # Make a GET request to the API
        response = requests.get(base_api_url + f'sites/{site_uuid}/')
        response.raise_for_status()  # Check for HTTP errors
        site = response.json()  # Convert the response to JSON

    except requests.exceptions.RequestException as e:
        # In case of an error, display an error message
        site = {}
        print(f"Error while retrieving site {site_id}: {e}")

    # Render the template with the site details
    return render(request, 'client/site_detail.html', {'site': site})
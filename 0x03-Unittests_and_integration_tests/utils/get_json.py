import requests

def get_json(url):
    """Fetch JSON content from a given URL."""
    response = requests.get(url)
    return response.json()

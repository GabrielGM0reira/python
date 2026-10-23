import requests

# Find city coordinates
def get_location(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if "results" not in data:
            return None
        location = data["results"][0]
        return (
            location["name"],
            location["latitude"],
            location["longitude"]
        )
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
        return None
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None
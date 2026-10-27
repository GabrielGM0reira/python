import requests

# Get weather data for the given coordinates
def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "temperature_unit": "celsius",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None
    
# Get 7 day forecast
def get_forecast(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "forecast_days": 7,
        "timezone": "auto",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

# Weather description
def get_weather_description(code):
    if code == 0:
        return "Clear sky"
    elif code in [1, 2, 3]:
        return "Mainly clear"
    elif code in [45, 48]:
        return "Fog"
    elif code in [51, 53, 55]:
        return "Drizzle"
    elif code in [61, 63, 65]:
        return "Rain"
    elif code in [71, 73, 75]:
        return "Snow"
    elif code in [80, 81, 82]:
        return "Rain showers"
    elif code in [95, 96, 99]:
        return "Thunderstorm"
    else:
        return "Unknown "
    
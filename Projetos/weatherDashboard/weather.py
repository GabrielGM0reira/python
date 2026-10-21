import requests

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
    
def celcius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32
        
city = input("Enter a city name: ")
location = get_location(city)
if location is None:
    print("Location not found.")
else:
    city_name, latitude, longitude = location
    weather = get_weather(latitude, longitude)
    if weather is None: 
        print("Weather data not found.")
    else:
        try:
            unit = input("Choose temperature unit (C/F): ").strip().upper()
            if unit not in ["C", "F"]:
                raise ValueError("Invalid temperature unit. Please choose 'C' or 'F'.")
    
            current = weather["current"]
            humidity = current["relative_humidity_2m"]
            windspeed = current["wind_speed_10m"]
            temperature = current["temperature_2m"]
            description = get_weather_description(current["weather_code"])
            print("=" * 40)
            print("DASHBOARD")
            print("=" * 40)
            print(f"Weather in {city_name}:")
            if unit == "F":
                temperature = celcius_to_fahrenheit(temperature)
                print(f"Temperature: {temperature:.2f}°F")
            else:
                print(f"Temperature: {temperature:.2f}°C")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {windspeed} km/h")
            print(f"Description: {description}")
            print("=" * 40)
        except KeyError as e:
            print(f"Missing data in weather response: {e}")
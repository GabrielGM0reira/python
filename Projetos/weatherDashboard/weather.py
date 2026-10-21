import requests

def get_location(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    if "results" not in data:
        return None
    location = data["results"][0]
    return (
        location["name"],
        location["latitude"],
        location["longitude"]
    )

def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "temperature_unit": "celsius",
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    return data

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
    current = weather["current"]
    humidity = current["relative_humidity_2m"]
    windspeed = current["wind_speed_10m"]
    temperature = current["temperature_2m"]
    description = get_weather_description(current["weather_code"])
    unit = input("Choose temperature unit (C/F): ").strip().upper()

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
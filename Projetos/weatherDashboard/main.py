from location import get_location
from weather import get_weather, get_weather_description
from utilities import celcius_to_fahrenheit

# Main program
while True: 
    # Prompt user for city name
    city = input("Enter a city name: ")
    if city.lower() == "exit":
        print("Exiting the program.")
        break
    
    #Find city coordinates
    location = get_location(city)
    if location is None:
        print("Location not found.")
        continue
    city_name, latitude, longitude = location
    
    # Get weather data for the given coordinates
    weather = get_weather(latitude, longitude)
    if weather is None: 
        print("Weather data not found.")
        continue
    
    try:
        current = weather["current"]
        humidity = current["relative_humidity_2m"]
        windspeed = current["wind_speed_10m"]
        temperature = current["temperature_2m"]
        description = get_weather_description(current["weather_code"])
    except KeyError:
        print("Error: Missing expected weather data.")
        continue
    
    # Prompt user for temperature unit
    while True:
        unit = input("Choose temperature unit (C/F): ").upper()
        if unit in ["C", "F"]:
            break
        print("Invalid unit. Please enter 'C' for Celsius or 'F' for Fahrenheit.")
        
    # convert temperature
    if unit == "F":
        display_temperature = celcius_to_fahrenheit(temperature)
        symbol = "°F"
    else:
        display_temperature = temperature
        symbol = "°C" 
    
    # Display weather information
    print("=" * 40)
    print(" WEATHER DASHBOARD")
    print("=" * 40)
    print(f"City: {city_name}")
    print(f"Temperature: {display_temperature:.2f} {symbol}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {windspeed} km/h")
    print(f"Description: {description}")
    print("=" * 40)
        
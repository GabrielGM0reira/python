import tkinter as tk
from tkinter import ttk, messagebox

from location import get_location
from weather import get_weather, get_weather_description, get_forecast
from utilities import celcius_to_fahrenheit, show_temperature_graph

# Global variables

graph_dates = []
graph_max_temperatures = []
graph_min_temperatures = []
graph_symbol = "°C"

# Get Weather 

def get_weather_data():
    global graph_dates
    global graph_max_temperatures
    global graph_min_temperatures
    global graph_symbol
        
    # Get city name
    city = city_entry.get().strip()
    
    if city == "":
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    #Find city coordinates
    location = get_location(city)
    if location is None:
        messagebox.showerror("Location Error", "City not found.")
        return
    city_name, latitude, longitude = location
    
    # Get current weather 
    weather = get_weather(latitude, longitude)
    if weather is None: 
        messagebox.showerror("Weather Error", "Weather data not found.")
        return
    
    try:
        #get current weather data
        current = weather["current"]
        
        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        windspeed = current["wind_speed_10m"]
        weather_code = current["weather_code"]
        
        description = get_weather_description(weather_code)
        
        # Ask selected temperature unit
        unit = unit_var.get()
        
        if unit == "F":
            display_temperature = celcius_to_fahrenheit(temperature)
            symbol = "°F"
        else:
            symbol = "°C"
            
        # display current weather 
        city_label.config(text=city_name)
        temperature_label.config(text=f"{round(display_temperature if unit == 'F' else temperature, 1)} {symbol}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {windspeed} km/h")
        condition_label.config(text=description)

    # Get 7-day forecast
        forecast = get_forecast(latitude, longitude)
        if forecast is None:
            messagebox.showerror("Forecast Error", "Forecast data not found.")
            return

        try: 
            # Extract forecast data
            daily = forecast["daily"]
            
            dates = daily["time"]
            max_temps = daily["temperature_2m_max"]
            min_temps = daily["temperature_2m_min"]
            weather_codes = daily["weather_code"]
            
            #Covert temperatures if needed
            if unit == "F":
                max_temperatures = [
                    celcius_to_fahrenheit(temp) for temp in max_temps
                ]
                min_temperatures = [
                    celcius_to_fahrenheit(temp) for temp in min_temps
                ]
            else:
                max_temperatures = max_temps
                min_temperatures = min_temps

            # clear previous graph data
            for item in forecast_table.get_children():
                forecast_table.delete(item)
            
            # Add forecast data to the table
            for i in range(len(dates)):
                description = get_weather_description(weather_codes[i])
                forecast_table.insert(
                    "",
                    "end",
                    values=(
                        dates[i],
                        f"{round(max_temperatures[i], 1)} {symbol}",
                        f"{round(min_temperatures[i], 1)} {symbol}",
                        description,
                    ) 
                )
            # Save graph data
            graph_dates = dates
            graph_max_temperatures = max_temperatures
            graph_min_temperatures = min_temperatures
            graph_symbol = symbol
            graph_button.config(state=tk.NORMAL)
            
        except KeyError:
            messagebox.showerror("Forecast Error", "Error: Missing expected forecast data.")
            return

    except (KeyError, TypeError):
        messagebox.showerror("Weather Error", "Error: Missing expected weather data.")

#Show graph 
def display_graph():
    if not graph_dates:
        
        messagebox.showwarning(
            "Graph Error", 
            "No forecast data available to display the graph."
        )
        return
        
    show_temperature_graph(
        graph_dates, 
        graph_max_temperatures, 
        graph_min_temperatures, 
        graph_symbol
        )
        
# Clear Dashboard
def clear_dashboard():
    global graph_dates, graph_max_temperatures, graph_min_temperatures, graph_symbol
    
    #clear city entry
    city_entry.delete(0, tk.END)
    
    #reset current weather 
    city_label.config(text="City")
    temperature_label.config(text="-- °C")
    condition_label.config(text="Condition")
    humidity_label.config(text="Humidity: N/A")
    wind_label.config(text="Wind Speed: N/A")
    
    #clear forecast table
    for item in forecast_table.get_children():
        forecast_table.delete(item)
        
    #disable graph button
    graph_button.config(state=tk.DISABLED)
    
    #reset temperature unit
    unit_var.set("C")
    
    # clear graph data
    graph_dates = []
    graph_max_temperatures = []
    graph_min_temperatures = []
    graph_symbol = "°C"
    
# Create Main Window
root = tk.Tk()

root.title("Weather Dashboard")
root.geometry("900x700")

root.resizable(False, False)

# Title

title_label = tk.Label(
    root, 
    text="Weather Dashboard", 
    font=("Helvetica", 24, "bold")
)

title_label.pack(pady=20)

# City Search

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Enter City:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10)
city_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
city_entry.grid(row=0, column=1, padx=10)

# Temperature Unit 

unit_var = tk.StringVar(value="C")
unit_frame = tk.Frame(root)
unit_frame.pack(pady=10)

tk.Label(unit_frame, text="Select Temperature Unit:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

tk.Radiobutton(
    unit_frame,
    text="Celsius (°C)",
    variable=unit_var,
    value="C").pack(side=tk.LEFT)
  
tk.Radiobutton(
    unit_frame,
    text="Fahrenheit (°F)",
    variable=unit_var,
    value="F").pack(side=tk.LEFT)
    
# Buttons

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

get_button = tk.Button(
    button_frame,
    text="Get Weather",
    command=get_weather_data,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=5
)
get_button.grid(row=0, column=0, padx=5)
      
graph_button = tk.Button(
    button_frame,
    text="Temperature Graph",
    command=display_graph,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=5,
    state="disabled"
)
graph_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(
    button_frame,
    text='clear',
    command=clear_dashboard,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=5
)
clear_button.grid(row=0, column=2, padx=5)

# Current Weather

weather_frame = tk.LabelFrame(
    root,
    text="Current Weather",
    font=("Helvetica", 12, "bold"),
    padx=20,
    pady=15
)
weather_frame.pack(
    padx=30,
    pady=15,
    fill="x"
)

city_label = tk.Label(
    weather_frame,
    text="City",
    font=("Helvetica", 16, "bold")
)
city_label.pack()

temperature_label = tk.Label(
    weather_frame,
    text="-- °C",
    font=("Helvetica", 35, "bold")
)
temperature_label.pack(pady=5)

condition_label = tk.Label(
    weather_frame,
    text="Condition",
    font=("Helvetica", 15)
)
condition_label.pack(pady=5)
details_frame = tk.Frame(weather_frame)
details_frame.pack(pady=10)

humidity_label = tk.Label(
    details_frame,
    text="Humidity: --%",
    font=("Helvetica", 11)
)
humidity_label.grid(row=0, column=0, padx=30)

wind_label = tk.Label(
    details_frame,
    text="Wind Speed: -- km/h",
    font=("Helvetica", 11)
)
wind_label.grid(row=0, column=1, padx=30)

# 7-Day Forecast Title

forecast_title = tk.Label(
    root,
    text="7-Day Forecast",
    font=("Helvetica", 16, "bold")
)
forecast_title.pack(pady=10, padx=5)

# 7-Day Forecast Table

table_frame = tk.Frame(root)

table_frame.pack(padx=30, fill="x")
columns = ("Date", "Max Temp", "Min Temp", "Condition")

forecast_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=7
)

forecast_table.heading("Date", text="Date")
forecast_table.heading("Condition", text="Condition")
forecast_table.heading("Max Temp", text="Max Temp")
forecast_table.heading("Min Temp", text="Min Temp")
forecast_table.column("Date", width=150, anchor="center")
forecast_table.column("Condition", width=250, anchor="center")
forecast_table.column("Max Temp", width=150, anchor="center")
forecast_table.column("Min Temp", width=150, anchor="center")
forecast_table.pack(side="left", fill="x")

# Start Application

root.mainloop()
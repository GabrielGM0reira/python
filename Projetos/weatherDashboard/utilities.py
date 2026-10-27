import matplotlib.pyplot as plt

# Method conversion
def celcius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def show_temperature_graph(dates, max_temperatures, min_temperatures, unit):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, max_temperatures, marker='o', label='Max Temperature')
    plt.plot(dates, min_temperatures, marker='s', label='Min Temperature')
    plt.title(f'7-Day Temperature Forecast')
    plt.xlabel('Date')
    plt.ylabel(f'Temperature ({unit})')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
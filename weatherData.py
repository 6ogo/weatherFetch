# Import necessary libraries
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily
import pandas as pd

# Set time period
start = datetime(2022, 1, 1)
end = datetime(2025, 3, 24)

# Define coordinates for the regions in Sweden
regions = {
    'Stockholm': Point(59.3293, 18.0686, 0),
    'Göteborg och Bohuslän': Point(57.7089, 11.9746, 0),
    'Skåne': Point(55.6050, 13.0038, 0),
    'Uppsala': Point(59.8586, 17.6389, 0),
    'Östgöta': Point(58.4108, 15.6214, 0),
    'Södermanland': Point(59.1984, 16.6113, 0),
    'Halland': Point(56.6745, 12.8570, 0),
    'Kalmar': Point(56.6616, 16.3616, 0),
    'Kronoberg': Point(56.9292, 14.7135, 0),
    'Blekinge': Point(56.2780, 15.4220, 0),
    'Gotland': Point(57.6366, 18.2926, 0),
    'Värmland': Point(59.3793, 13.5036, 0),
    'Dalarna': Point(60.4858, 15.4376, 0),
    'Gävleborg': Point(60.6749, 17.1413, 0),
    'Västernorrland': Point(62.3908, 17.3069, 0),
    'Jämtland': Point(63.1770, 14.6362, 0),
    'Västerbotten': Point(64.7500, 20.9500, 0),
    'Norrbotten': Point(66.8309, 20.3997, 0),
    'Jönköping': Point(57.7826, 14.1618, 0),
    'Älvsborg': Point(58.1624, 12.5655, 0),
    'Skaraborg': Point(58.3912, 13.8450, 0),
    'Bergslagen': Point(60.0000, 15.0000, 0),
    'Göinge-Kristianstad': Point(56.0294, 14.1567, 0)
}

# Create an empty DataFrame to store the data
all_data = pd.DataFrame()

# Loop through each region and fetch data
for region_name, region_point in regions.items():
    # Get daily data for the region
    data = Daily(region_point, start, end)
    data = data.fetch()

    # Check if data is empty
    if data.empty:
        continue

    # Add region name to the data
    data['Region'] = region_name

    # Reset index to include date as a column
    data.reset_index(inplace=True)

    # Select relevant columns and rename them
    data = data[['time', 'Region', 'tavg', 'prcp']]
    data.columns = ['Date', 'Region', 'Temp', 'Prcp']

    # Append the data to the all_data DataFrame
    all_data = pd.concat([all_data, data], ignore_index=True)

# Save the data to an Excel file
all_data.to_excel('Sweden_Weather_Data.xlsx', index=False)
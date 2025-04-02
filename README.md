# Weather Data Fetcher
## Overview
This project fetches daily weather data for various regions in Sweden for the period from January 1, 2022, to March 24, 2025. The data includes average temperature, precipitation, and sunshine duration. The fetched data is then saved to an Excel file.

## Data Source

The weather data is sourced from the [Meteostat](https://meteostat.net/) service, which provides access to historical weather and climate data. Meteostat collects data from various sources including weather stations, satellites, and other meteorological services.

## Libraries Used
- `datetime`: For handling date and time operations.
- `matplotlib.pyplot`: For plotting data.
- `meteostat`: For fetching weather data.
- `pandas`: For data manipulation and saving data to an Excel file.

## Installation
To run this project, you need to have Python installed along with the necessary libraries. You can install the required libraries using `pip`:

```bash
pip install matplotlib meteostat pandas openpyxl
```

## Usage
Set the timeperiod:
```python
start = datetime(2022, 1, 1)
end = datetime(2025, 3, 24)
```

Define coordinates for the regions (for Sweden in code):
```python
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
```

Fetch and process the data:
```python
all_data = pd.DataFrame()

for region_name, region_point in regions.items():
    data = Daily(region_point, start, end)
    data = data.fetch()

    if data.empty:
        continue

    data['Region'] = region_name
    data.reset_index(inplace=True)
    data = data[['time', 'Region', 'tavg', 'prcp']]
    data.columns = ['Date', 'Region', 'Temp', 'Prcp']
    all_data = pd.concat([all_data, data], ignore_index=True)
```

Save the data to an Excel file:
```python
all_data.to_excel('Sweden_Weather_Data.xlsx', index=False)
```

## Output
The script will generate an Excel file named Sweden_Weather_Data.xlsx containing the following columns:
Date: The date of the observation.
Region: The region name.
Temp: The average temperature in °C.
Prcp: The daily precipitation total in mm.

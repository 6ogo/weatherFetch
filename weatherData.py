# Import necessary libraries
from datetime import datetime
# import matplotlib.pyplot as plt # Not used in this snippet
from meteostat import Point, Daily
import pandas as pd
import logging # Import logging to potentially capture library warnings better

# Configure meteostat logging level (optional, might help capture more details)
# logging.basicConfig(level=logging.DEBUG) # Uncomment for very verbose output
# logging.getLogger('meteostat').setLevel(logging.WARNING) # Default is usually WARNING

# Set time period
start = datetime(2022, 1, 1)
end = datetime(2025, 3, 24)

# Define coordinates for the regions in Sweden
# Using the standardized names from the previous example's output
regions_coordinates = {
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
    'Jämtland': Point(63.1792, 14.6357),
    'Västerbotten': Point(64.7500, 20.9500, 0),
    'Norrbotten': Point(65.58381853174998, 22.156047098542405, 0),
    'Jönköping': Point(57.7826, 14.1618, 0),
    'Älvsborg': Point(58.1624, 12.5655, 0),
    'Skaraborg': Point(58.3912, 13.8450, 0),
    'Bergslagen': Point(59.6004350028211, 16.526784483212424, 0),
    'Göinge-Kristianstad': Point(56.0294, 14.1567, 0)
}

# Create an empty DataFrame to store the data
all_data = pd.DataFrame()
failed_regions = [] # Keep track of regions that failed

print("Starting data fetch process...")

# Loop through each region and fetch data
for region_name, region_point in regions_coordinates.items():
    print(f"\n--- Attempting to fetch data for: {region_name} ---")
    try:
        # Get daily data for the region
        data_fetcher = Daily(region_point, start, end)
        print(f"  Fetching data from meteostat for {region_name}...")
        data = data_fetcher.fetch() # This is the line that might trigger the warning or an error

        # Check if data is empty AFTER the fetch attempt
        if data.empty:
            print(f"  WARNING: No data returned for {region_name} after fetch attempt.")
            failed_regions.append((region_name, "No data returned"))
            continue # Skip to the next region

        print(f"  Successfully fetched data for {region_name} (found {len(data)} rows).")

        # Add region name to the data
        data['Region'] = region_name

        # Reset index to include date as a column
        data.reset_index(inplace=True)

        # Select relevant columns and rename them
        # Check if columns exist
        cols_to_select = ['time', 'Region']
        rename_map = {'time': 'Date', 'Region': 'Region'}
        if 'tavg' in data.columns:
            cols_to_select.append('tavg')
            rename_map['tavg'] = 'Temp'
        else:
             print(f"  Note: 'tavg' column missing for {region_name}.")
        if 'prcp' in data.columns:
            cols_to_select.append('prcp')
            rename_map['prcp'] = 'Prcp'
        else:
            print(f"  Note: 'prcp' column missing for {region_name}.")


        data = data[cols_to_select]
        data.rename(columns=rename_map, inplace=True)

        # Append the data to the all_data DataFrame
        all_data = pd.concat([all_data, data], ignore_index=True)
        print(f"  Data processed and appended for {region_name}.")

    except Exception as e:
        # Catch any exception during Daily() or fetch()
        print(f"  ERROR fetching or processing data for {region_name}: {e}")
        failed_regions.append((region_name, str(e)))
        # The library warning might appear before or after this error message in the console.
        continue # Skip to the next region

# --- Reporting ---
print("\n--- Fetch Summary ---")
if not all_data.empty:
    print(f"Successfully fetched data for {len(all_data['Region'].unique())} region(s).")
    output_filename = 'Sweden_Weather_Data_Regions.xlsx'
    try:
        all_data.to_excel(output_filename, index=False, engine='openpyxl')
        print(f"Combined data saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving data to Excel: {e}")
        print("Attempting to save as CSV instead...")
        output_filename_csv = 'Sweden_Weather_Data_Regions.csv'
        try:
             all_data.to_csv(output_filename_csv, index=False, encoding='utf-8-sig')
             print(f"Combined data successfully saved to {output_filename_csv}")
        except Exception as e_csv:
             print(f"Error saving data to CSV: {e_csv}")

else:
    print("No data was successfully fetched for any region.")

if failed_regions:
    print("\nRegions with fetch/processing issues:")
    for name, reason in failed_regions:
        print(f"  - {name}: {reason}")
else:
    print("\nNo regions encountered fetch/processing issues.")

print("\nScript finished.")
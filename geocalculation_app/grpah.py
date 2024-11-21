# import numpy as np
# import matplotlib.pyplot as plt
# import csv

# # Define grid parameters
# latitude_start = 15.0
# latitude_end = 18.0
# longitude_start = 78.0
# longitude_end = 81.0
# row_step = 0.08333000
# col_step = 0.08333000

# # Read values from CSV file
# values = []
# with open('revarse.csv', 'r') as file:
#     reader = csv.reader(file)
#     for i, row in enumerate(reader):
#         if i < 37:  # Exclude the last row
#             if row: 
#                 values.extend(map(float, row[0].split()))  

# # Adjust the number of steps
# num_steps = 37
# latitudes = np.linspace(latitude_start, latitude_end, num_steps)
# longitudes = np.linspace(longitude_start, longitude_end, num_steps)

# # Create meshgrid
# lon_grid, lat_grid = np.meshgrid(longitudes, latitudes)

# # Plot grid points with values
# plt.figure(figsize=(15, 10))
# for lat, lon, val in zip(lat_grid.flatten(), lon_grid.flatten(), values):
#     plt.scatter(lon, lat, color='red', zorder=5)  # scatter points with lower zorder
#     plt.annotate(f'{val:.5f}', (lon, lat), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='black')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('Grid Points Visualization with Values')
# plt.grid(True)
# plt.show()

import numpy as np
import matplotlib.pyplot as plt
import csv

def dms_to_decimal(degrees, minutes=0, seconds=0):
    return degrees + minutes / 60 + seconds / 3600

# Convert DMS to decimal degrees
height_start_dd = dms_to_decimal(0, 5)  # 0 degrees, 5 minutes
height_end_dd = dms_to_decimal(0, 5) 

# Define grid parameters
latitude_start = 8.000000
latitude_end = 12.999800
longitude_start = 74.500000
longitude_end = 77.499880
row_step = height_start_dd
col_step = height_end_dd

# Calculate number of steps based on step size
num_rows = int((latitude_end - latitude_start) / row_step) + 1
num_cols = int((longitude_end - longitude_start) / col_step) + 1

print(f"Calculated num_rows: {num_rows}, num_cols: {num_cols}")

# Initialize values list
values = []

# Read values from CSV file
with open('keraladatagrid.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        row_values = list(map(float, row[0].split()))
        values.extend(row_values)

# Print the total number of values read
total_values = len(values)
print(f"Total values read from CSV: {total_values}")

# Calculate expected number of values
expected_values = num_rows * num_cols
print(f"Expected values: {expected_values}")

# Check if the total number of values matches the expected shape
if total_values != expected_values:
    print(f"Warning: Expected {expected_values} values but found {total_values} values in the CSV. Trimming the excess values.")
    values = values[:expected_values]

# Reshape values to match latitudes and longitudes
values = np.array(values).reshape(num_rows, num_cols)

# Create latitudes and longitudes arrays
latitudes = np.linspace(latitude_start, latitude_end, num_rows)
longitudes = np.linspace(longitude_start, longitude_end, num_cols)

# Plot heatmap
plt.figure(figsize=(15, 10))
plt.imshow(values, extent=[longitude_start, longitude_end, latitude_start, latitude_end], cmap='hot', aspect='auto', origin='lower')
plt.colorbar(label='Values')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Heatmap Visualization')
plt.grid(True)

# Save the plot as an image file
plt.savefig('heatmap_kerala.png')



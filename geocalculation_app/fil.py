import csv

def read_grid_from_csv(filename):
    grid = {'data': []}
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        rows = list(reader)  # Read all rows into a list
        for row in rows:  # Iterate over rows
            values = [float(val) for val in row if val.strip()]  # Ignore empty strings
            grid['data'].append(values)
    grid['Latitude(start)'] = 15.000000
    grid['longitude(start)'] = 78.000000
    grid['lat_step'] = 0.08333000
    grid['lon_step'] = 0.08333000
    return grid

def get_grid_point(lat, lon, grid):
    lat_index = int((lat - grid['Latitude(start)']) / grid['lat_step'])
    lon_index = int((lon - grid['longitude(start)']) / grid['lon_step'])
    return lat_index, lon_index

def get_value_from_grid(grid, lat, lon):
    lat_index, lon_index = get_grid_point(lat, lon, grid)
    print("lat_index:", lat_index)
    print("lon_index:", lon_index)
    
    # Check if the calculated index is within the grid range
    if 0 <= lat_index < len(grid['data']) and 0 <= lon_index < len(grid['data'][0]):
        # If the point is within the grid, return the value at that point
        return grid['data'][lat_index][lon_index]
    else:
        # If the point is outside the grid, calculate the average of the nearest 4 points
        values = []
        for i in range(lat_index - 1, lat_index + 2):
            for j in range(lon_index - 1, lon_index + 2):
                # Check if the calculated index is within the grid range
                if 0 <= i < len(grid['data']) and 0 <= j < len(grid['data'][0]):
                    values.append(grid['data'][i][j])
        # Calculate the average of the values
        avg_value = sum(values) / len(values)
        return avg_value

def get_value_from_csv(filename, lat, lon):
    grid = read_grid_from_csv(filename)
    return get_value_from_grid(grid, lat, lon)

# Example usage
filename = 'data.csv'  # Replace 'your_file.csv' with the path to your CSV file
lat = 15.000000
lon = 78.000000

result = get_value_from_csv(filename, lat, lon)
print("Value from grid:", result)

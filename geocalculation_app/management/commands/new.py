import csv
from django.core.management.base import BaseCommand
from geocalculation_app.models import GridData, GridPoint
import math

class Command(BaseCommand):
    help = 'Assigns values within Bihar boundaries'

    def handle(self, *args, **options):
        def dms_to_decimal(degrees, minutes=0, seconds=0):
            return degrees + minutes / 60 + seconds / 3600

        # Convert DMS to decimal degrees
        height_start_dd = dms_to_decimal(0, 5)  # 0 degrees, 5 minutes
        height_end_dd = dms_to_decimal(0, 5)    # 0 degrees, 5 minutes

        print(f"Height start (decimal degrees): {height_start_dd}")
        print(f"Height end (decimal degrees): {height_end_dd}")

        # Define the grid boundaries for India
        india_latitude_start = 0.000000
        india_latitude_end = 40.000000
        india_longitude_start = 60.000000
        india_longitude_end = 110.000000
        height_start = height_start_dd
        height_end = height_end_dd

        # Define the grid boundaries for Bihar
        bihar_latitude_start = 8.000000
        bihar_latitude_end = 12.999800
        bihar_longitude_start = 74.500000
        bihar_longitude_end = 77.499880

        # Retrieve existing GridData instance for India
        try:
            grid_data = GridData.objects.get(
                latitude_start=india_latitude_start,
                latitude_end=india_latitude_end,
                longitude_start=india_longitude_start,
                longitude_end=india_longitude_end,
                height_start=height_start,
                height_end=height_end
            )
        except GridData.DoesNotExist:
            self.stdout.write(self.style.ERROR("GridData instance for India not found. Populate India grid first."))
            return

        # Path to the CSV file containing Bihar grid points data
        csv_file_path = 'keraladatagrid.csv'

        # Read grid points data from the CSV file for Bihar
        bihar_values = {}
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            for row_index, row in enumerate(reader):
                values = row[0].split()  # Split the row by spaces
                for col_index, value in enumerate(values):
                    value = value.strip()
                    try:
                        value = float(value)
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"Unable to convert '{value}' to float. Skipping."))
                        continue
                    # Store the value in a dictionary with (row_index, col_index) as the key
                    bihar_values[(row_index, col_index)] = value

        # Calculate the number of rows and columns for the India grid
        num_rows = math.ceil((india_latitude_end - india_latitude_start) / height_start)
        num_cols = math.ceil((india_longitude_end - india_longitude_start) / height_end)

        # Loop through each grid point for India and assign values based on Bihar grid if within Bihar boundaries
        for row_index in range(num_rows):
            for col_index in range(num_cols):
                # Calculate latitude and longitude for each point based on grid boundaries and index
                latitude = india_latitude_start + row_index * height_start
                longitude = india_longitude_start + col_index * height_end

                # Determine if the current point falls within Bihar
                if (bihar_latitude_start <= latitude <= bihar_latitude_end and
                        bihar_longitude_start <= longitude <= bihar_longitude_end):
                    # Calculate the corresponding row and column index in the Bihar grid
                    bihar_row_index = int((latitude - bihar_latitude_start) / height_start)
                    bihar_col_index = int((longitude - bihar_longitude_start) / height_end)
                    value = bihar_values.get((bihar_row_index, bihar_col_index), float('nan'))
                else:
                    value = float('nan')

                # Find existing GridPoint instance for the current latitude and longitude within India grid
                try:
                    grid_point = GridPoint.objects.get(grid_data=grid_data, latitude=latitude, longitude=longitude)
                except GridPoint.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"GridPoint at ({latitude}, {longitude}) does not exist. Skipping."))
                    continue

                # Assign value and save GridPoint instance
                grid_point.value = value
                grid_point.save()

                # Print the updated grid point
                self.stdout.write(self.style.SUCCESS(f"Grid point updated: {grid_point}"))

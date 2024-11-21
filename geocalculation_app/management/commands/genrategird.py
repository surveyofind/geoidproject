import csv
from django.core.management.base import BaseCommand
from geocalculation_app.models import GridData, GridPoint
import math

class Command(BaseCommand):
    help = 'Populates grid points data'

    def handle(self, *args, **options):
        # Define the grid boundaries for India
        india_latitude_start = 24.000000   
        india_latitude_end = 28.000000
        india_longitude_start = 83.000000
        india_longitude_end = 88.500000
        height_start = 0.08333000
        height_end = 0.08333000
        grid_data, created = GridData.objects.get_or_create(
            latitude_start=india_latitude_start,
            latitude_end=india_latitude_end,
            longitude_start=india_longitude_start,
            longitude_end=india_longitude_end,
            height_start=height_start,
            height_end=height_end
        )

        # Path to the CSV file containing Bihar grid points data
        csv_file_path = 'bihardata.csv'

        # Read grid points data from the CSV file
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

        for row_index in range(num_rows):
            for col_index in range(num_cols):
                # Calculate latitude and longitude for each point based on grid boundaries and index
                latitude = india_latitude_start + row_index * height_start
                longitude = india_longitude_start + col_index * height_end
                
                grid_point = GridPoint.objects.create(
                    grid_data=grid_data,
                    latitude=latitude,
                    longitude=longitude,
                    value=value
                )

                # Print the created grid point
                self.stdout.write(self.style.SUCCESS(f"Grid point created: {grid_point}"))



# bihar_latitude_start = 24.000000
#         bihar_latitude_end = 28.000000
#         bihar_longitude_start = 83.000000
#         bihar_longitude_end = 88.500000
# import csv
# from django.core.management.base import BaseCommand
# from geocalculation_app.models import GridData, GridPoint
# from cryptography.fernet import Fernet
# import base64

# class Command(BaseCommand):
#     help = 'Populates grid points data'

#     def handle(self, *args, **options):
#         # Load the secret key from a file
#         with open('secret.key', 'rb') as key_file:
#             key = key_file.read()

#         # Initialize Fernet with the key
#         cipher_suite = Fernet(key)

#         # Create or retrieve GridData instance
#         grid_data, created = GridData.objects.get_or_create(
#             latitude_start=15.000000,
#             latitude_end=18.000000,
#             longitude_start=78.000000,
#             longitude_end=81.000000,
#             height_start=0.08333000,
#             height_end=0.08333000
#         )

#         # Path to the CSV file containing grid points data
#         csv_file_path = 'revarse.csv'

#         # Read grid points data from the CSV file
#         with open(csv_file_path, 'r') as file:
#             reader = csv.reader(file)
#             for row_index, row in enumerate(reader):
#                 values = row[0].split()  # Split the row by spaces
#                 for col_index, value in enumerate(values):
#                     # Strip any whitespace characters from the value
#                     value = value.strip()
#                     try:
#                         # Convert each value to float
#                         value = float(value)
#                     except ValueError:
#                         # If conversion fails, print a warning and continue to the next value
#                         self.stdout.write(self.style.WARNING(f"Unable to convert '{value}' to float. Skipping."))
#                         continue

#                     # Encrypt the value
#                     encrypted_value = cipher_suite.encrypt(str(value).encode())

#                     # Convert encrypted value to a format suitable for storage (e.g., base64)
#                     encrypted_value_base64 = base64.urlsafe_b64encode(encrypted_value).decode('utf-8')

#                     # Calculate latitude and longitude for each point based on grid boundaries and index
#                     latitude = grid_data.latitude_start + row_index * grid_data.height_start
#                     longitude = grid_data.longitude_start + col_index * grid_data.height_end

#                     # Create GridPoint instance and save it
#                     grid_point = GridPoint.objects.create(
#                         grid_data=grid_data,
#                         latitude=latitude,
#                         longitude=longitude,
#                         value=encrypted_value_base64  # Save the encrypted value
#                     )

#                     # Print the created grid point
#                     self.stdout.write(self.style.SUCCESS(f"Grid point created: {grid_point}"))

import csv
from django.core.management.base import BaseCommand
from geocalculation_app.models import GridData, GridPoint

class Command(BaseCommand):
    help = 'Populates grid points data'

    def handle(self, *args, **options):
        # Create or retrieve GridData instance
        grid_data, created = GridData.objects.get_or_create(
            latitude_start=21.500000,
            latitude_end=27.500000,
            longitude_start=85.500000,
            longitude_end=90.000000,
            height_start=0.08333000,
            height_end=0.08333000
        )

        # Path to the CSV file containing grid points data
        csv_file_path = 'WestBengaldata.csv'

        # Read grid points data from the CSV file
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            for row_index, row in enumerate(reader):
                values = row[0].split()  # Split the row by spaces
                for col_index, value in enumerate(values):
                    # Strip any whitespace characters from the value
                    value = value.strip()
                    try:
                        # Convert each value to float
                        value = float(value)
                    except ValueError:
                        # If conversion fails, print a warning and continue to the next value
                        self.stdout.write(self.style.WARNING(f"Unable to convert '{value}' to float. Skipping."))
                        continue

                    # Calculate latitude and longitude for each point based on grid boundaries and index
                    latitude = grid_data.latitude_start + row_index * grid_data.height_start
                    longitude = grid_data.longitude_start + col_index * grid_data.height_end

                    # Create GridPoint instance and save it
                    grid_point = GridPoint.objects.create(
                        grid_data=grid_data,
                        latitude=latitude,
                        longitude=longitude,
                        value=value  # Directly store the value without encryption
                    )

                    # Print the created grid point
                    self.stdout.write(self.style.SUCCESS(f"Grid point created: {grid_point}"))

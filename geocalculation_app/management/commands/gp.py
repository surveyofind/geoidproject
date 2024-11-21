# import csv
# from django.core.management.base import BaseCommand
# from geocalculation_app.models import GridData, GridPoint

# class Command(BaseCommand):
#     help = 'Populates grid points data'

#     def handle(self, *args, **options):
#         def dms_to_decimal(degrees, minutes=0, seconds=0):
#             return degrees + minutes / 60 + seconds / 3600

        
#         height_start_dd = dms_to_decimal(0, 5) 
#         height_end_dd = dms_to_decimal(0, 5)    
#         print(height_end_dd)
#         print(height_start_dd)
   
#         grid_data, created = GridData.objects.get_or_create(
#             latitude_start=0.000000,
#             latitude_end=40.000000,
#             longitude_start=60.000000,
#             longitude_end=110.000000,
#             height_start=height_start_dd,
#             height_end=height_end_dd
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

#                     # Calculate latitude and longitude for each point based on grid boundaries and index
#                     latitude = grid_data.latitude_start + row_index * grid_data.height_start
#                     longitude = grid_data.longitude_start + col_index * grid_data.height_end

#                     # Create GridPoint instance and save it
#                     grid_point = GridPoint.objects.create(
#                         grid_data=grid_data,
#                         latitude=latitude,
#                         longitude=longitude,
#                         value=value  # Use the original value
#                     )

#                     # Print the created grid point
#                     self.stdout.write(self.style.SUCCESS(f"Grid point created: {grid_point}"))



import csv
from django.core.management.base import BaseCommand
from geocalculation_app.models import GridData, GridPoint
import math

class Command(BaseCommand):
    help = 'Populates grid points data for the entire region of India'

    def handle(self, *args, **options):
        def dms_to_decimal(degrees, minutes=0, seconds=0):
            return degrees + minutes / 60 + seconds / 3600

       
        height_start_dd = dms_to_decimal(0, 5)  
        height_end_dd = dms_to_decimal(0, 5)    

        print(f"Height start (decimal degrees): {height_start_dd}")
        print(f"Height end (decimal degrees): {height_end_dd}")

       
        grid_data, created = GridData.objects.get_or_create(
            latitude_start=27.600000,
            latitude_end=31.000000,
            longitude_start=74.400000,
            longitude_end=77.600000,
            height_start=height_start_dd,
            height_end=height_end_dd,
            # height_start=0.08333,
            # height_end=0.08333
        ) 
        csv_file_path = 'haryana.csv'
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            for row_index, row in enumerate(reader):
                values = row[0].split()  
                for col_index, value in enumerate(values):
                    value = value.strip()
                    try:
                       
                        if value.lower() == 'nan':
                            value = math.nan
                        else:
                            value = float(value)
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"Unable to convert '{value}' to float. Skipping."))
                        continue
                    latitude = grid_data.latitude_start + row_index * grid_data.height_start
                    longitude = grid_data.longitude_start + col_index * grid_data.height_end
                    if abs(latitude - round(latitude)) < 1e-10:
                        latitude = round(latitude)
                    if abs(longitude - round(longitude)) < 1e-10:
                        longitude = round(longitude)

                   
                    grid_point = GridPoint.objects.create(
                        grid_data=grid_data,
                        latitude=latitude,
                        longitude=longitude,
                        value=value,
                        state ='HARYANA'    
                    )

                    # Print the created grid point
                    self.stdout.write(self.style.SUCCESS(f"Grid point created: {grid_point}"))





# from django.core.management.base import BaseCommand
# from geocalculation_app.models import GridData, GridPoint
# import math

# class Command(BaseCommand):
#     help = 'Populates grid points data for the entire region of India with NaN values'

#     def handle(self, *args, **options):
#         def dms_to_decimal(degrees, minutes=0, seconds=0):
#             return degrees + minutes / 60 + seconds / 3600

#         # Convert DMS to decimal degrees
#         height_start_dd = dms_to_decimal(0, 5)  # 0 degrees, 5 minutes
#         height_end_dd = dms_to_decimal(0, 5)    # 0 degrees, 5 minutes

#         print(f"Height start (decimal degrees): {height_start_dd}")
#         print(f"Height end (decimal degrees): {height_end_dd}")

#         # Create or retrieve GridData instance
#         grid_data, created = GridData.objects.get_or_create(
#             latitude_start=0.000000,
#             latitude_end=40.000000,
#             longitude_start=60.000000,
#             longitude_end=110.000000,
#             height_start=height_start_dd,
#             height_end=height_end_dd
#         )

#         # Generate grid points
#         latitude = grid_data.latitude_start
#         while latitude <= grid_data.latitude_end:
#             longitude = grid_data.longitude_start
#             while longitude <= grid_data.longitude_end:
#                 # Ensure the latitude and longitude values are aligned to the grid correctly
#                 if abs(latitude - round(latitude)) < 1e-10:
#                     latitude = round(latitude)
#                 if abs(longitude - round(longitude)) < 1e-10:
#                     longitude = round(longitude)

#                 # Create GridPoint instance and save it with NaN val ue
#                 grid_point = GridPoint.objects.create(
#                     grid_data=grid_data,
#                     latitude=latitude,
#                     longitude=longitude,
#                     value=math.nan  # Set the value to NaN
#                 )

#                 # Print the created grid point
#                 self.stdout.write(self.style.SUCCESS(f"Grid point created: {grid_point}"))

#                 # Increment longitude
#                 longitude += grid_data.height_end

#             # Increment latitude
#             latitude += grid_data.height_start




# import csv
# from django.core.management.base import BaseCommand
# from geocalculation_app.models import GridData, GridPoint

# class Command(BaseCommand):
#     help = 'Updates grid points data for the Bihar region with values from a CSV file'

#     def handle(self, *args, **options):
#         # Define Bihar latitude and longitude range
#         bihar_latitude_start = 24.000000
#         bihar_latitude_end = 28.000000
#         bihar_longitude_start = 83.000000
#         bihar_longitude_end = 88.500000

#         # Define height step in decimal degrees (5 minutes)
#         height_step_dd = 1 / 12

#         # Path to the CSV file containing grid points data for Bihar
#         csv_file_path = 'bihardata.csv'

#         # Read grid points data from the CSV file and update Bihar region
#         with open(csv_file_path, 'r') as file:
#             reader = csv.reader(file)
#             latitude = bihar_latitude_start
#             for row_index, row in enumerate(reader):
#                 values = row[0].split()  # Split the row by spaces
#                 longitude = bihar_longitude_start
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

#                     # Ensure longitude does not exceed bihar_longitude_end
#                     if longitude > bihar_longitude_end:
#                         break  # Skip values beyond Bihar longitude range

#                     # Find the grid point and update its value
#                     grid_point = GridPoint.objects.filter(
#                         grid_data__latitude_start__lte=latitude,
#                         grid_data__latitude_end__gte=latitude,
#                         grid_data__longitude_start__lte=longitude,
#                         grid_data__longitude_end__gte=longitude,
#                         latitude=latitude,
#                         longitude=longitude
#                     ).first()
#                     if grid_point:
#                         grid_point.value = value
#                         grid_point.save()
#                         self.stdout.write(self.style.SUCCESS(f"Grid point updated: {grid_point}"))

#                     # Increment longitude
#                     longitude += height_step_dd

#                 # Increment latitude
#                 latitude += height_step_dd
#                 if latitude > bihar_latitude_end:
#                     break
#                 # End of inner loop
#             # End of outer loop




# import csv
# from django.core.management.base import BaseCommand
# from geocalculation_app.models import GridData, GridPoint
# import math

# class Command(BaseCommand):
#     help = 'Populates grid points data for the entire region of India with NaN values and updates Bihar region from CSV'

#     def handle(self, *args, **options):
#         def dms_to_decimal(degrees, minutes=0, seconds=0):
#             return degrees + minutes / 60 + seconds / 3600

#         # Convert DMS to decimal degrees
#         height_start_dd = dms_to_decimal(0, 5)  # 0 degrees, 5 minutes
#         height_end_dd = dms_to_decimal(0, 5)    # 0 degrees, 5 minutes

#         print(f"Height start (decimal degrees): {height_start_dd}")
#         print(f"Height end (decimal degrees): {height_end_dd}")

#         # Create or retrieve GridData instance
#         grid_data, created = GridData.objects.get_or_create(
#             latitude_start=0.000000,
#             latitude_end=40.000000,
#             longitude_start=60.000000,
#             longitude_end=110.000000,
#             height_start=height_start_dd,
#             height_end=height_end_dd
#         )

#         # Generate grid points for all of India with NaN values
#         latitude = grid_data.latitude_start
#         while latitude <= grid_data.latitude_end:
#             longitude = grid_data.longitude_start
#             while longitude <= grid_data.longitude_end:
#                 # Ensure the latitude and longitude values are aligned to the grid correctly
#                 if abs(latitude - round(latitude)) < 1e-10:
#                     latitude = round(latitude)
#                 if abs(longitude - round(longitude)) < 1e-10:
#                     longitude = round(longitude)

#                 # Create GridPoint instance and save it with NaN value
#                 grid_point = GridPoint.objects.create(
#                     grid_data=grid_data,
#                     latitude=latitude,
#                     longitude=longitude,
#                     value=math.nan  # Set the value to NaN
#                 )

#                 # Print the created grid point
#                 self.stdout.write(self.style.SUCCESS(f"Grid point created: {grid_point}"))

#                 # Increment longitude
#                 longitude += grid_data.height_end

#             # Increment latitude
#             latitude += grid_data.height_start

#         # Define Bihar latitude and longitude range
#         bihar_latitude_start = 0.000000
#         bihar_latitude_end = 2.999800
#         bihar_longitude_start = 74.000000
#         bihar_longitude_end = 77.499880

#         # Path to the CSV file containing grid points data for Bihar
#         csv_file_path = 'keraladatagrid.csv'

#         # Read grid points data from the CSV file and update Bihar region
#         with open(csv_file_path, 'r') as file:
#             reader = csv.reader(file)
#             latitude = bihar_latitude_start
#             for row_index, row in enumerate(reader):
#                 values = row[0].split()  # Split the row by spaces
#                 longitude = bihar_longitude_start
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

#                     # Find the grid point and update its value
#                     grid_point = GridPoint.objects.filter(
#                         grid_data=grid_data,
#                         latitude=latitude,
#                         longitude=longitude
#                     ).first()
#                     if grid_point:
#                         grid_point.value = value
#                         grid_point.save()
#                         self.stdout.write(self.style.SUCCESS(f"Grid point updated: {grid_point}"))

#                     # Increment longitude
#                     longitude += height_end_dd
#                 # Increment latitude
#                 latitude += height_start_dd



# import csv
# from django.core.management.base import BaseCommand
# from geocalculation_app.models import GridData, GridPoint
# import math

# class Command(BaseCommand):
#     help = 'Populates grid points data'


#     def handle(self, *args, **options):
#         def dms_to_decimal(degrees, minutes=0, seconds=0):
#             return degrees + minutes / 60 + seconds / 3600

#         # Convert DMS to decimal degrees
#         height_start_dd = dms_to_decimal(0, 5)  # 0 degrees, 5 minutes
#         height_end_dd = dms_to_decimal(0, 5)    # 0 degrees, 5 minutes

#         print(f"Height start (decimal degrees): {height_start_dd}")
#         print(f"Height end (decimal degrees): {height_end_dd}")
#         # Define the grid boundaries for India
#         india_latitude_start = 0.000000
#         india_latitude_end = 40.000000
#         india_longitude_start = 60.000000
#         india_longitude_end = 110.000000
#         height_start = height_start_dd
#         height_end = height_end_dd

#         # Define the grid boundaries for Bihar
#         bihar_latitude_start = 8.000000
#         bihar_latitude_end = 12.999800
#         bihar_longitude_start = 74.500000
#         bihar_longitude_end = 77.499880

#         # Create or retrieve GridData instance for India
#         grid_data, created = GridData.objects.get_or_create(
#             latitude_start=india_latitude_start,
#             latitude_end=india_latitude_end,
#             longitude_start=india_longitude_start,
#             longitude_end=india_longitude_end,
#             height_start=height_start,
#             height_end=height_end
#         )

#         # Path to the CSV file containing Bihar grid points data
#         csv_file_path = 'keraladatagrid.csv'

#         # Read grid points data from the CSV file
#         bihar_values = {}
#         with open(csv_file_path, 'r') as file:
#             reader = csv.reader(file)
#             for row_index, row in enumerate(reader):
#                 values = row[0].split()  # Split the row by spaces
#                 for col_index, value in enumerate(values):
#                     value = value.strip()
#                     try:
#                         value = float(value)
#                     except ValueError:
#                         self.stdout.write(self.style.WARNING(f"Unable to convert '{value}' to float. Skipping."))
#                         continue
#                     # Store the value in a dictionary with (row_index, col_index) as the key
#                     bihar_values[(row_index, col_index)] = value

#         # Calculate the number of rows and columns for the India grid
#         num_rows = math.ceil((india_latitude_end - india_latitude_start) / height_start)
#         num_cols = math.ceil((india_longitude_end - india_longitude_start) / height_end)

#         for row_index in range(num_rows):
#             for col_index in range(num_cols):
#                 # Calculate latitude and longitude for each point based on grid boundaries and index
#                 latitude = india_latitude_start + row_index * height_start
#                 longitude = india_longitude_start + col_index * height_end

#                 # Determine if the current point falls within Bihar
#                 if (bihar_latitude_start <= latitude <= bihar_latitude_end and
#                         bihar_longitude_start <= longitude <= bihar_longitude_end):
#                     # Calculate the corresponding row and column index in the Bihar grid
#                     bihar_row_index = int((latitude - bihar_latitude_start) / height_start)
#                     bihar_col_index = int((longitude - bihar_longitude_start) / height_end)
#                     value = bihar_values.get((bihar_row_index, bihar_col_index), float('nan'))
#                 else:
#                     value = float('nan')

#                 # Create GridPoint instance and save it
#                 grid_point = GridPoint.objects.create(
#                     grid_data=grid_data,
#                     latitude=latitude,
#                     longitude=longitude,
#                     value=value
#                 )

#                 # Print the created grid point
#                 self.stdout.write(self.style.SUCCESS(f"Grid point created: {grid_point}"))


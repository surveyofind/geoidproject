from django.core.management.base import BaseCommand
from geocalculation_app.models import GridData, GridPoint
import matplotlib.pyplot as plt

class Command(BaseCommand):
    help = 'Populates grid points data'

    def handle(self, *args, **options):
        # Retrieve grid points data from the database
        grid_points = GridPoint.objects.filter(grid_data__latitude_start=15.0,  # Example filter based on grid data
                                               grid_data__longitude_start=78.0)

        # Define lists to store latitude, longitude, and values
        latitudes = []
        longitudes = []
        values = []

        # Extract data from grid points queryset
        for grid_point in grid_points:
            latitudes.append(grid_point.latitude)
            longitudes.append(grid_point.longitude)
            values.append(grid_point.value)

        # Create scatter plot
        plt.figure(figsize=(10, 8))
        plt.scatter(longitudes, latitudes, c=values, cmap='viridis', edgecolors='k', alpha=0.7)
        plt.colorbar(label='Value')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Grid Points Visualization')
        plt.grid(True)
        plt.show()

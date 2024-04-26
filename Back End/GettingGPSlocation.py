import geocoder
import geopy.distance
import math
import pandas as pd
from geopy.distance import geodesic

def get_location():
    g = geocoder.ip('me')
    return g.latlng  # Return the coordinates

# Your location
user_loc = get_location()


# Read the Excel file
df = pd.read_excel("C:\Users\jorge\Downloads\new_aed_locations.xlsx")

# Initialize an empty list to store the points within the circle
points_within_circle = []

# Loop through each row in the DataFrame
# Loop through each row in the DataFrame
for i, row in df.iterrows():
    # Get the longitude and latitude from the row
    lon, lat = row.iloc[0], row.iloc[1]
    print(lon, lat)
    if lon < -90 or lon > 90 or lat < -90 or lat > 90:
        continue
    # Iterate over the range of distances from 1 km to 10 km
    for distance in range(1, 11):
        # Calculate the distance from the point to the center of the circle
        distance_km = geodesic((lat, lon), coords).km
        # If the distance is less than or equal to the current distance, add the point to the list
        if distance_km <= distance:
            points_within_circle.append((lon, lat, distance))

        #if sum of points >23 points, then stop the for loop

points_within_circle = points_within_circle[:23]
# Print the points within the circle
for i, point in enumerate(points_within_circle, 1):
    print(f"Point {i}: {point}")
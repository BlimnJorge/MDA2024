import requests
import json
import quickest_destination from FindingNearestAed.ipynb
# Your Google Maps API key
api_key = "YOUR_API_KEY"

# Your destination (point B)
destination = [4.2, 50.8]  # Replace with your actual coordinates

# Convert the coordinates to strings
origin_str = f"{coords[1]},{coords[0]}"
destination_str = f"{destination[1]},{destination[0]}"

# Make a request to the Google Maps Directions API
response = requests.get(
    "https://maps.googleapis.com/maps/api/directions/json",
    params={
        "origin": origin_str,
        "destination": destination_str,
        "key": api_key
    }
)

# Parse the response
data = response.json()

# Print the directions
for i, route in enumerate(data["routes"][0]["legs"][0]["steps"], 1):
    print(f"Step {i}: {route['html_instructions']}")
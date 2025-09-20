import requests

# Google Maps Elevation API
API_KEY = "YOUR_API_KEY"
path = "33.6844,73.0479|32.0836,72.6711"  # Tx|Rx coordinates

url = f"https://maps.googleapis.com/maps/api/elevation/json?path={path}&samples=50&key={API_KEY}"

response = requests.get(url).json()

profile = [(p["location"]["lat"], p["location"]["lng"], p["elevation"]) for p in response["results"]]

print(profile[:5])  # first few points

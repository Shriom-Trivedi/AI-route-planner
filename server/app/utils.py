import requests

# Reverse geocode utility
def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    headers = {"User-Agent": "RoutePlannerAgent"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("display_name", f"{lat},{lon}")
    return f"{lat},{lon}"

# Create a summarized route string
def build_route_summary(coordinates):
    summary = []
    for i, (lon, lat) in enumerate(coordinates):
        place = reverse_geocode(lat, lon)
        summary.append(f"Stop {i+1}: {place}")
    return "\n".join(summary)

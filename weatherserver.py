from mcp.server.fastmcp import FastMCP
from geopy.geocoders import Nominatim
import json
import requests
import re

mcp = FastMCP("weather-mcp")


def extract_location(query: str) -> str:
    # Normalize the query
    query = query.lower().strip()

    # Common patterns
    patterns = [
        r"weather\s+(in|at|for|about)?\s*(.+)",
        r"what(?:'s| is)? the weather (in|at|for|about)?\s*(.+)",
        r"how is the weather (in|at|for|about)?\s*(.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            location = match.group(2)
            return location.strip(" ?.,").title()

    match = re.match(r"(.*?)(?:\s+weather)?$", query)
    if match:
        location = match.group(1)
        return location.strip().title()

    # fallback
    return query.title()  # Try returning the whole thing capitalized


def get_lat_lon(location_name):
    geolocator = Nominatim(user_agent="weather-mcp/1.0")
    location = geolocator.geocode(location_name, timeout=10)

    if location:
        return location.latitude, location.longitude, location.address

    return None, None, None



def get_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )

    try:
        r = requests.get(url, timeout=5)

        data = r.json()["current_weather"]
        units = r.json()["current_weather_units"]

        return {
            "temperature": str(data["temperature"]) + " " + units["temperature"],
            "windspeed": str(data["windspeed"]) + " " + units["windspeed"],
            "weathercode": data["weathercode"],
        }

    except Exception as e:
        raise RuntimeError(f"Error fetching weather data: {e}") from e
    


@mcp.tool("weather")
def weather(query: str) -> str:
    """Fetches the current weather for a given location."""
    location_name = extract_location(query)
    lat, lon, resolved_address = get_lat_lon(location_name)

    if lat is None or lon is None:
        return f"Could not find location: {location_name}"

    weather_data = get_weather(lat, lon)
    result = {
        "location": location_name,
        "resolved_address": resolved_address,
        "latitude": lat,
        "longitude": lon,
        **weather_data,
    }
    return (
        f"Weather for {location_name} ({resolved_address}): "
        f"temperature {weather_data['temperature']}, "
        f"wind {weather_data['windspeed']}, "
        f"weather code {weather_data['weathercode']}. "
        f"Details: {json.dumps(result)}"
    )


if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        print("Server stopped.")

        


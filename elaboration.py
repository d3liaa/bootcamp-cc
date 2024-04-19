import requests
from datetime import datetime
import json

# Function to get data from API
def get_data_today():
    limit = "20"
    where_statement = "pcode.in.%28%22ASM_00000183%22%2C%22ASM_00000182%22%29"
    now = datetime.now()
    time_start = now.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")[:-3]
    time_end = now.strftime("%Y-%m-%dT%H:%M:%S")[:-3]
    
    print(f"Start Time: {time_start}")
    print(f"End Time: {time_end}")
    
    response = requests.get(
        f'https://mobility.api.opendatahub.com/v2/flat/EChargingPlug/%2A/{time_start}/{time_end}?limit={limit}&offset=0&where={where_statement}&shownull=false&distinct=true&timezone=UTC')
    
    print(f"Response Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Failed to retrieve data")
        return None
    return response.json()

# Function to parse data and create structured format with timestamps
def create_station_structure(data):
    if data is None:
        return []

    station_dict = {}

    for entry in data.get('data', []):
        station_id = entry.get('pcode')
        plug_id = entry.get('scode')
        timestamp = entry.get('_timestamp')
        is_active = entry.get('mvalue') == 1

        if station_id not in station_dict:
            station_dict[station_id] = {}

        if plug_id not in station_dict[station_id]:
            station_dict[station_id][plug_id] = {}
        
        station_dict[station_id][plug_id][timestamp] = is_active

    # Convert dictionary to list format expected
    stations = [{"stationID": station_id, **plugs} for station_id, plugs in station_dict.items()]
    
    return stations

# Example usage
if __name__ == "__main__":
    api_data = get_data_today()
    if api_data:
        structured_data = create_station_structure(api_data)
        print(json.dumps(structured_data, indent=2))
    else:
        print("No data to process")

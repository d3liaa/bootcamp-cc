import requests
from datetime import datetime, timedelta

# Parameters
time_start = "2024-01-01"
time_end = "2024-01-07"
limit = "20"
where_statement = "scode.in.%28%22ASM_00000183%22%2C%22ASM_00000182%22%29"

# Function to get data from API
def get_data():
    response = requests.get(f'https://mobility.api.opendatahub.com/v2/flat/EChargingStation/%2A/{time_start}/{time_end}?limit={limit}&offset=0&where={where_statement}&shownull=false&distinct=true&timezone=UTC')
    return response.json()


def get_data_today():
    # Get current date and time
    now = datetime.now()

    # Format for start time: 00:00 of the current day
    time_start = now.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")[:-3]

    # Format for end time: current date and time
    time_end = now.strftime("%Y-%m-%dT%H:%M:%S")[:-3]

    print(time_start)
    print(time_end)
    response = requests.get(f'https://mobility.api.opendatahub.com/v2/flat/EChargingStation/%2A/{time_start}/{time_end}?limit={limit}&offset=0&where={where_statement}&shownull=false&distinct=true&timezone=UTC')
    return response.json()

# Main function
# def main():
#     data = get_data_today()
#     print(data)


# Run the main function
# if __name__ == "__main__":
#     main()


# mvalue == 0, means that it is in use (it is the free value count)


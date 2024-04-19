import requests

# Parameters
time_start = "2024-01-01"
time_end = "2024-01-07"
limit = "20"
where_statement = "scode.in.%28%22ASM_00000183%22%2C%22ASM_00000182%22%29"

# Function to get data from API
def get_data():
    response = requests.get(f'https://mobility.api.opendatahub.com/v2/flat/EChargingStation/%2A/{time_start}/{time_end}?limit={limit}&offset=0&where={where_statement}&shownull=false&distinct=true&timezone=UTC')
    return response.json()

# Main function
def main():
    data = get_data()
    print(data)


# Run the main function
if __name__ == "__main__":
    main()



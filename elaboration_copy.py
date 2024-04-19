import requests

# Parameters
time_start = "2024-01-01"
time_end = "2024-01-07"
limit = "20"
where_statement = "scode.in.%28%22ASM_00000183%22%2C%22ASM_00000182%22%29"

# Function to get data from API
def get_data():
    response = requests.get(f'https://mobility.api.opendatahub.com/v2/flat/EChargingStation/*/{time_start}/{time_end}?limit={limit}&offset=0&where={where_statement}&shownull=false&distinct=true&timezone=UTC')
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from API.")
        return None

# Main function
def main():
    data = get_data()
    if data:
        print("Data:", data)  # Print out the data to understand its structure

        total = 0
        not_operational = 0
        used = 0
        not_used = 0
        unknown = 0
        outlets_not_operational = 0
        outlets_used = 0
        outlets_not_used = 0
        outlets_unknown = 0
        curr_is_used = False
        last_pcode = None

        NOT_OPERATIONAL_STATES = ["TEMPORARYUNAVAILABLE", "FAULT"]  
        OPERATIONAL_STATES = ["ACTIVE", "AVAILABLE", "OCCUPIED"] 

        def sort_station_states(station_states):
            station_states_sorted = sorted(station_states, key=lambda x: (x['pcode'], x['mvalue'], x['pmetadata']['state']))
            return station_states_sorted


        for rec in response:
            curr_outlet_count = len(rec["smetadata.outlets"])

            total_plugs += 1
            outlets_total += curr_outlet_count

            # mvalue == 0, means that it is in use (it is the free value count)
            if rec["mvalue"] == 0:
                curr_is_used = True

            if rec["pcode"] != last_pcode:
                total += 1

            is_state_known = rec["mvalue"] >= 0

            if rec["pmetadata"]["state"] in NOT_OPERATIONAL_STATES:
                outlets_not_operational += curr_outlet_count
                if rec["pcode"] != last_pcode:
                    not_operational += 1
            elif rec["pmetadata"]["state"] in OPERATIONAL_STATES and is_state_known:
                if curr_is_used:
                    outlets_used += curr_outlet_count
                    if rec["pcode"] != last_pcode:
                        used += 1
                else:
                    outlets_not_used += curr_outlet_count
                    if rec["pcode"] != last_pcode:
                        not_used += 1
            else:
                outlets_unknown += curr_outlet_count
                if rec["pcode"] != last_pcode:
                    unknown += 1

            curr_is_used = False
            last_pcode = rec["pcode"]


        print("Total:", total)
        print("Not Operational:", not_operational)
        print("Used:", used)
        print("Not Used:", not_used)
        print("Unknown:", unknown)
        print("Outlets Not Operational:", outlets_not_operational)
        print("Outlets Used:", outlets_used)
        print("Outlets Not Used:", outlets_not_used)
        print("Outlets Unknown:", outlets_unknown)
    else:
        print("No data fetched. Exiting...")








# Run the main function
if __name__ == "__main__":
    main()

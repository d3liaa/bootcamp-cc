import pandas as pd
from elaboration import stations
import requests


def times_day_availability(stations):
    total_plugs = 0
    total_true_count = 0
    
    for station in stations:
        plugs = station['plugs']
        true_count = sum(plugs.values())
        total_plugs += len(plugs)
        total_true_count += true_count

    if total_plugs > 0:
        average_availability = total_true_count / total_plugs
    else:
        average_availability = 0

    return average_availability

        
def main():
    average_availability = times_day_availability(stations)
    print("Average availability of plugs:", average_availability)

if __name__ == "__main__":
    main()

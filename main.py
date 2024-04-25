import csv
import requests


def make_cities(filename):
    cities = []

    # Read city data from CSV file
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            city = {
                "name": row[0],
                "latitude": float(row[1]),
                "longitude": float(row[2])
            }
            cities.append(city)
    return cities


def fetch_charging_stations(latitude, longitude, distance=100):
    api_key = 'e00cb487-943f-4208-a607-8a5594f63524'  # key that i got after sign up
    """
    Fetch EV charging stations using Open Charge Map API.
    
    Parameters:
    latitude (float): Latitude of the center point.
    longitude (float): Longitude of the center point.
    distance (int): Search radius in meters (default is 5000m).
    api_key (str): Your Open Charge Map API key (optional).

    Returns:
    list: List of EV charging stations.
    """
    api_url = f"https://api.openchargemap.io/v3/poi/?output=json&latitude={latitude}&longitude={longitude}&distance={distance}"
    if api_key:
        api_url += f"&key={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            print("Failed to fetch charging stations: Unexpected response format")
            return None
    else:
        print("Failed to fetch charging stations:", response.status_code)
        return None


def write_to_csv(charging_stations, filename="charging_stations.csv"):
    """
    Write charging station data to a CSV file.

    Parameters:
    charging_stations (list): List of charging stations.
    filename (str): Name of the CSV file to write to (default is 'charging_stations.csv').
    """

    with open(filename, mode='a', newline='', encoding='utf-8') as file:  # 'a' for append mode
        writer = csv.writer(file)
        # Write data
        for station in charging_stations:
            writer.writerow([station.get('AddressInfo', {}).get('Title', ''),
                             station.get('AddressInfo', {}).get('Latitude', ''),
                             station.get('AddressInfo', {}).get('Longitude', ''),
                             station.get('AddressInfo', {}).get('AddressLine1', ''), ])


def remove_duplicates():
    filename = "/Users/elieh/PycharmProjects/pythonProject4/first_charging_stations.csv"
    dic_stations = {}  # Dictionnary of all the stations name

    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            if row[0] not in dic_stations:
                dic_stations[row[0]] = [row[0], row[1], row[2],
                                        row[3]]  # Add the entire station data to the dictionnary

    open("clean_charging_stations.csv", mode='w', newline='', encoding='utf-8')  # delete previous data
    with open("clean_charging_stations.csv", mode='a', newline='', encoding='utf-8') as file:  # Use 'a' for append mode

        writer = csv.writer(file)
        writer.writerow(["Name", "Latitude", "Longitude", "Adress"])
        # Write data
        for key in dic_stations:
            writer.writerow([dic_stations[key][0],
                             dic_stations[key][1],
                             dic_stations[key][2],
                             dic_stations[key][3]])


def main():
    filename = "il.csv"  # Name of the CSV file with city data
    cities = make_cities(filename)
    output_filename = "first_charging_stations.csv"  # Name of the first output CSV file

    open(output_filename, mode='w', newline='', encoding='utf-8')  # delete previous data

    # Fetch charging stations for each city and write to output CSV file
    for city in cities:
        print(f"Fetching charging stations for {city['name']}...")
        charging_stations = fetch_charging_stations(city['latitude'], city['longitude'], 500)
        if charging_stations:
            write_to_csv(charging_stations, output_filename)
            print(f"Charging stations data for {city['name']} has been written to {output_filename}")
        else:
            print(f"Failed to fetch charging stations data for {city['name']}.")

    remove_duplicates()


if __name__ == "__main__":
    main()

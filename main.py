import pandas as pd
import random
from datetime import datetime, timedelta
import json

data = json.load(open("osm-world-airports.geojson"))
airports = [feature["properties"] for feature in data["features"]]
european_countries = [
    "Albania",
    "Andorra",
    "Armenia",
    "Austria",
    "Azerbaijan",
    "Belgium",
    "Bosnia and Herzegovina",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Georgia",
    "Germany",
    "Greece",
    "Hungary",
    "Iceland",
    "Ireland",
    "Italy",
    "Kazakhstan",
    "Kosovo",
    "Latvia",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Moldova",
    "Monaco",
    "Montenegro",
    "Netherlands",
    "North Macedonia",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "San Marino",
    "Serbia",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "Switzerland",
    "Turkey",
    "United Kingdom",
    "Vatican City",
]
filtered_airports = list(filter(lambda x: x["country"] in european_countries, airports))

airport_df = pd.DataFrame(filtered_airports)
airport_df = airport_df.drop(
    columns=[
        "name_fr",
        "icao",
        "wikipedia",
        "wikidata",
        "website",
        "phone",
        "operator",
        "description",
        "id",
        "source",
        "other_tags",
    ]
)

european_airlines = [
    {"name": "Lufthansa", "code": "LH"},
    {"name": "British Airways", "code": "BA"},
    {"name": "Air France", "code": "AF"},
    {"name": "KLM Royal Dutch Airlines", "code": "KL"},
    {"name": "Iberia", "code": "IB"},
    {"name": "Aeroflot", "code": "SU"},
    {"name": "Scandinavian Airlines (SAS)", "code": "SK"},
    {"name": "Turkish Airlines", "code": "TK"},
    {"name": "Finnair", "code": "AY"},
    {"name": "Swiss International Air Lines", "code": "LX"},
    {"name": "Aer Lingus", "code": "EI"},
    {"name": "Alitalia", "code": "AZ"},
    {"name": "Austrian Airlines", "code": "OS"},
    {"name": "Brussels Airlines", "code": "SN"},
    {"name": "LOT Polish Airlines", "code": "LO"},
    {"name": "TAP Air Portugal", "code": "TP"},
    {"name": "Norwegian Air Shuttle", "code": "DY"},
    {"name": "Wizz Air", "code": "W6"},
    {"name": "Eurowings", "code": "EW"},
    {"name": "Pegasus Airlines", "code": "PC"},
]


def generate_flight_number():
    airline = random.choice(european_airlines)
    return f"{airline['code']}-{random.randint(100, 999)}"


airbus_models = ["A220", "A320", "A330", "A350", "A380"]
boeing_models = ["737", "747", "777", "787"]


def generate_airplane_name():
    manufacturer = random.choice(["Airbus", "Boeing"])

    if manufacturer == "Airbus":
        model = random.choice(airbus_models)
    else:
        model = random.choice(boeing_models)

    return f"{manufacturer} {model}"


# European Major Airports
ema = pd.DataFrame(
    [
        {"name": "Heathrow Airport", "code": "LHR", "country": "United Kingdom"},
        {"name": "Charles de Gaulle Airport", "code": "CDG", "country": "France"},
        {"name": "Frankfurt Airport", "code": "FRA", "country": "Germany"},
        {"name": "Amsterdam Schiphol Airport", "code": "AMS", "country": "Netherlands"},
        {"name": "Zurich Airport", "code": "ZRH", "country": "Switzerland"},
        {"name": "Barcelona-El Prat Airport", "code": "BCN", "country": "Spain"},
        {
            "name": "Leonardo da Vinci–Fiumicino Airport",
            "code": "FCO",
            "country": "Italy",
        },
        {"name": "Dublin Airport", "code": "DUB", "country": "Ireland"},
        {"name": "Copenhagen Airport", "code": "CPH", "country": "Denmark"},
        {"name": "Vienna International Airport", "code": "VIE", "country": "Austria"},
        {"name": "Athens International Airport", "code": "ATH", "country": "Greece"},
        {"name": "Moscow Sheremetyevo Airport", "code": "SVO", "country": "Russia"},
        {"name": "Oslo Airport", "code": "OSL", "country": "Norway"},
        {"name": "Warsaw Chopin Airport", "code": "WAW", "country": "Poland"},
        {"name": "Stockholm Arlanda Airport", "code": "ARN", "country": "Sweden"},
        {"name": "Lisbon Airport", "code": "LIS", "country": "Portugal"},
        {"name": "Brussels Airport", "code": "BRU", "country": "Belgium"},
        {"name": "Helsinki-Vantaa Airport", "code": "HEL", "country": "Finland"},
        {"name": "Istanbul Airport", "code": "IST", "country": "Turkey"},
    ]
)


# Function to generate random flight paths with start times
def generate_flight_paths_with_times(airport_df):
    flights = []

    # Generate random flight paths
    for index, origin in airport_df.iterrows():
        for d_index, destination in airport_df.iterrows():
            if origin["iata"] != destination["iata"]:
                num_flights = random.randint(
                    1, 10 if origin["iata"] in ema["code"] else 3
                )

                for day in range(20):

                    start_time = datetime(
                        2024,
                        2,
                        1 + day,
                        hour=random.randint(0, 23),
                        minute=random.choice([0, 30]),
                    )
                    flight_path = {
                        "Origin": origin["iata"],
                        "Destination": destination["iata"],
                        "Start_time": start_time,
                        "Flight_number": generate_flight_number(),
                        "Plane": generate_airplane_name(),
                    }

                    flights.append(flight_path)

    flights_df = pd.DataFrame(flights)

    return flights_df


flight_paths_with_times_df = generate_flight_paths_with_times(airport_df)

flight_paths_with_times_df.to_json("flights.json", orient="records")
airport_df.to_json('airports.json', orient='records')
pd.DataFrame(european_airlines).to_json('airlines.json', orient='records')

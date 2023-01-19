import argparse
import csv
import random
from math import radians, cos, sin, sqrt, atan2

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, nargs='?', default=None)
    return parser.parse_args()



def generate_random_places(n):
    random_places = []
    place_names = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "San Francisco", "Charlotte", "Indianapolis", "Seattle", "Denver", "Washington DC"]
    random.shuffle(place_names)
    for name in place_names:
        lat = random.randint(-90, 90)
        lon = random.randint(-180, 180)
        random_places.append((name, lat, lon))
    return random_places[:n]
        

def read_places(n=None):
    if n:
        # Generate n random places
        random_place = generate_random_places(n)
        return random_place
    else:
        # Read from places.csv
        with open("place.csv") as f:
            reader = csv.reader(f,delimiter=';')
            next(reader)
            return [(row[0],float(row[1]), float(row[2])) for row in reader]

def air_distance(p1, p2):
    # Convert to radians
    lat1, lon1 = radians(p1[1]), radians(p1[2])
    lat2, lon2 = radians(p2[1]), radians(p2[2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    # Earth radius = 6371 km
    return 6371 * c

def main():
    args = parse_args()
    n = args.n
    places = read_places(n)
    distances = []
    seen = set()
    
    for i in range(len(places)):
        for j in range(i+1, len(places)):
            p1 = places[i]
            p2 = places[j]
            if (p1, p2) in seen or (p2, p1) in seen:
                continue
            seen.add((p1, p2))
            distance = air_distance(p1, p2)
            distances.append((p1, p2, distance))
    
    # Sort by distance
    distances.sort(key=lambda x: x[2])
    total_distance = 0
    for (p1, p2, distance) in distances:
        total_distance += distance
        # use format()
        print(f"{p1[0] : <20}    {p2[0]: ^30}     {distance:.2f}km.")


    avg_distance = total_distance / len(distances)
    closest_pair = min(distances, key=lambda x: abs(x[2] - avg_distance))
   
    print(f"Average distance: {avg_distance:.2f}km. Closest pair: {closest_pair[0][0]} - {closest_pair[1][0]} {closest_pair[2]:.2f} km.")

if __name__ == "__main__":
    main()

import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance
from math import isnan


# using the address, find the geolocalization of the house
def get_lat_long(addr):
    #addr= "Via Console Marcello 20, Milano, MI" #test
    geolocator = Nominatim(user_agent="sbnc")
    location = geolocator.geocode(addr)
    if location is not None:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    return float("nan"), float("nan")

# compute the distance from the dome and drop NaN values
file = sys.argv[1] if len(sys.argv)>1 else "dataset.csv" # starting .csv, the new .csv will be saved as "<file_name>_updated.csv"
dome = (45.464161, 9.190335)
latitude = []
longitude = []
distance = []
df = pd.read_csv(file)
print(df.columns)
df = df.dropna(subset=['address'])

for addr in df["address"]:
    print(addr)
    [lat, lon] = get_lat_long(addr)
    latitude.append(lat)
    longitude.append(lon)
    if isnan(lat):
        dist = float("nan")
    else:
        dist = geopy.distance.geodesic((lat, lon), dome).km

    distance.append(dist)
    print([lat, lon, dist])

df["latitude"] = latitude
df["longitude"] = longitude
df["DFD"] = distance
df = df.dropna(subset=["DFD", "latitude", "longitude"])
df.to_csv(file[:-4]+'_updated.csv')

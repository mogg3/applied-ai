from sko.ACA import ACA_TSP
from math import sin, asin, cos, sqrt, atan2, radians
import regex as re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np


def get_data():
    # Scrapes the data
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome('./chromedriver', options=options)

    driver.get(
        "https://www.infoplease.com/world/geography/major-cities-latitude-longitude-and-corresponding-time-zones")
    elem = driver.find_element_by_id("A0001770")
    text = elem.text
    driver.close()
    return text


def get_cities(data):
    # Formats the data into a more convenient lookup table
    rows = data.split('\n')
    cities = []
    for row in rows[2:]:
        city = re.findall('[A-Za-z].*, [A-Za-z]*', row)
        latitude, longitude = re.findall('[0-9]{1,} [0-9]{1,} [SNWE]', row)
        cities.append({'city': city,
                       'latitude': latitude,
                       'longitude': longitude})
    return cities


def to_degrees(city):
    dms_to_deg = lambda deg, minutes, direction: (float(deg) + float(minutes) / 60) * (
        -1 if direction in ['W', 'S'] else 1)

    latitude = city['latitude']
    longitude = city['longitude']

    lat = dms_to_deg(*re.split('[ ]', latitude))
    long = dms_to_deg(*re.split('[ ]', longitude))

    return radians(lat), radians(long)


def calc_d(city1, city2):
    # calculates the distance between two coordinates
    lat1, lon1 = to_degrees(city1)
    lat2, lon2 = to_degrees(city2)

    R = 6372.8  # km

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (sin(dlat / 2) ** 2) + (cos(lat1) * cos(lat2) * (sin(dlon / 2) ** 2))
    c = 2 * asin(sqrt(a))

    distance = R * c
    return distance  # km


def get_distance_matrix(cities):
    # Generates a distance matrix from a list of cities with coordinates
    index_matrix = [[(i, j) for j in range(len(cities))] for i in range(len(cities))]

    distance_matrix = [[calc_d(cities[i_tup[0]], cities[i_tup[1]]) for i_tup in row] for row in index_matrix]
    return np.array([np.array(row) for row in distance_matrix])


def cal_total_distance(routine):
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])



# i = 0
# j = 7
#
# print(cities[i])
# print(cities[j])
# print(distance_matrix[i][j])


data = get_data()
cities = get_cities(data)
distance_matrix = get_distance_matrix(cities)


# TODO Add path back to 0

num_points = len(cities)
size_pop = 50
max_iter = 250

start = time.time()
aca = ACA_TSP(func=cal_total_distance,
              n_dim=num_points,
              size_pop=size_pop, max_iter=max_iter,
              distance_matrix=distance_matrix)

best_x, best_y = aca.run()
stop = time.time()

time_elapsed = stop - start

result = {'routine': best_x, 'distance': best_y,'time': time_elapsed, 'pop_size': size_pop, 'max_iter': max_iter}


print(f'Routine: {best_x}\n\nDistance: {round(best_y)}km\n\nTime: {round(time_elapsed)} sec\n\nPopulation size: {size_pop}\n\nMax iterations: {max_iter}')

import math
from . import vfs as v


def data_keywords():
    return [
        'time',
        'wind_speed',
        'average_wind_speed',
        'max_wind_speed1',
        'max_wind_speed2',
        'wind_direction',
        'temperature1',
        'temperature2',
        'humidity1',
        'humidity2',
        'air_pressure',
        'rain_flag',
        'dhumidity1',
        'dhumidity2',
    ]


def out_items():
    return [
        'temperature1',
        'humidity1',
        'temperature2',
        'humidity2',
        'air_pressure',
        'average_wind_speed',
        'wind_direction',
    ]


def wind_direction2octas(direction_degree):
    if direction_degree >= 360 or direction_degree < 0:
        direction_degree = direction_degree \
            - math.floor(direction_degree / 360) * 360
    direction_degree_shift = direction_degree + 360.0 / 16.0
    if direction_degree_shift < 45:
        return 'N'
    if direction_degree_shift < 90:
        return 'NE'
    if direction_degree_shift < 135:
        return 'E'
    if direction_degree_shift < 180:
        return 'SE'
    if direction_degree_shift < 225:
        return 'S'
    if direction_degree_shift < 270:
        return 'SW'
    if direction_degree_shift < 315:
        return 'W'
    return 'NW'


make_data = v.make_data


def find_data(time):
    data_list = make_data(time)
    timedelta_array = [abs(data['time'] - time) for data in data_list]
    min_index = timedelta_array.index(min(timedelta_array))
    return data_list[min_index]


def get_data(time, keywords=data_keywords()):
    data = find_data(time)
    return {key: value for key, value in data.items() if key in keywords}

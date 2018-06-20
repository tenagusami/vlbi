from ..weather import weather as w
from . import vfs as v


def keywords():
    return [
        'optical_depth_0', 'optical_depth_1', 'atmospheric_temperature',
        'receiver_temperature', 'system_temperature', 'band', 'misc'
    ]


def out_keywords():
    return [
        'time',
        'optical_depth_0',
        'receiver_temperature',
        'system_temperature',
        'band',
    ]


def weather_keywords():
    return [
        'temperature2',
        'humidity2',
        'air_pressure',
        'wind_direction',
        'average_wind_speed',
    ]


def add_weather_data(info):
    weather_data = w.get_data(info['time'], weather_keywords())
    info.update(weather_data)
    return info


def get(today):
    return [add_weather_data(info) for info in v.read(today)]


def info_list2lines_list(info_list):
    def string_convert(info, item):
        if item == 'time':
            return item + ': ' \
                + info[item].astimezone().strftime('%m/%d(%jd) %H:%MJST')
        return item + ': ' + str(info[item])

    def info2lines(info):
        return [string_convert(info, item) for item
                in out_keywords() + weather_keywords()]

    if not info_list:
        return [['no secZ data']]
    return [info2lines(info) for info in info_list]


def display(lines_list):
    print('===========\n  sec Z\n===========')
    if not lines_list:
        print('no sec Z data')
        return
    for lines in lines_list:
        for line in lines:
            print(line)
        else:
            print('-----------')

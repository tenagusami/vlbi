import datetime as d
import os
from . import vex as v
from ..utility import increment_day


def keywords():
    return [
        'observation_ID',
        'description',
        'start_time',
        'end_time',
        'PI_name',
        'contact_name',
        'band',
        'timestamp',
    ]


def daily_boundary_from_0hUT():
    return d.timedelta(hours=8)


def read_observations(date_from, date_until):
    transferred_file_paths_stat = v.get_files_between(date_from, date_until)
    observation_info_list = [
        v.read_obs_info(file_path, file_stat, keywords())
        for file_path, file_stat in transferred_file_paths_stat
    ]
    for file_path, file_stat in transferred_file_paths_stat:
        os.remove(file_path)
    return observation_info_list


def sort_observations(obs_info_list):
    return sorted(obs_info_list, key=lambda info: info['start_time'])


def filter_obs_today(obs_info_list, today, time_delta=d.timedelta(hours=0)):
    schedule_boundary_today = today + time_delta
    schedule_boundary_tomorrow = increment_day(schedule_boundary_today)

    def is_observation_today(info):
        return (info['start_time'] <= schedule_boundary_tomorrow
                and info['end_time'] > schedule_boundary_today)

    return [obs_info for obs_info in obs_info_list
            if is_observation_today(obs_info)]


def date_predicate(*args):
    return v.date_predicate(*args)


def get_observations(date_from, date_until):
    obs_info_list = read_observations(date_from, date_until)
    return sort_observations(obs_info_list)


def info_list2lines_list(info_list):
    def string_convert(info, item):
        if item == 'start_time' \
                or item == 'end_time':
            return item + ': ' \
                + info[item].astimezone().strftime('%m/%d(%jd) %H:%MJST')
        return item + ': ' + str(info[item])

    def info2lines(info):
        return [string_convert(info, item) for item in keywords()]

    if not info_list:
        return [['no observations']]
    return [info2lines(info) for info in info_list]


def display(lines_list):
    print('===========\n  Schedule\n===========')
    for lines in lines_list:
        for line in lines:
            print(line)
        else:
            print('-----------')

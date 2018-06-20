import os
from .. import utility as U
from ..log import log
from .. import operation as oper
from . import secZ


def remote_dir(today):
    return '/usr2/log/days' + '/' + today.strftime('%Y%j')


def remote_file_name(today):
    return today.strftime('%Y%j') + '.SECZ.log'


def make_data(line):
    def convert_value(keyword, value):
        if keyword == 'optical_depth_0':
            value = -U.round_float(value, 0.01)
        elif not keyword == 'band':
            value = int(U.round_float(value, 0))
        return value

    data_dict_tmp = {
        keyword: convert_value(keyword, value)
        for (keyword, value) in zip(secZ.keywords(), line[2].split())
    }
    data_dict_tmp['time'] = log.time_string2datetime(line[0])
    return {
        keyword: value
        for keyword, value in data_dict_tmp.items()
        if keyword in secZ.out_keywords()
    }


def read(today):
    try:
        file_name = remote_file_name(today)
        file_path, file_stat = oper.get_files(
            remote_dir(today), U.tmp_dir(),
            lambda fname: fname == file_name)[0]
    except (RuntimeError, IndexError):
        return []

    data_keyword = 'TSYS1'
    with open(file_path, 'r') as f:
        lines = [[
            key_value.strip().strip(";") for key_value in line.strip().split("/")
        ] for line in f.readlines() if data_keyword in line]
    os.remove(file_path)
    return [make_data(line) for line in lines]

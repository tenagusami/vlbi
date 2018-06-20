from ..log import log
from ..utility import round_float
from . import weather as w
from ..operation import get_command_output


def make_query_command(time):
    date_string = log.datetime2doy_string(time)
    # if not time:
    #    return 'ssh clock -f tail -n 1 /usr2/log/days/' + date_string \
    #        + '/' + date_string + '.WS.log'
    time_string = log.datetime2time_string(time)[0:-2]
    return 'ssh clock -f "grep ' + time_string + ' /usr2/log/days/' \
        + date_string + '/' + date_string + '.WS.log |grep -v SPDNOW"'


def get_log_lines(time):
    return get_command_output(make_query_command(time))


def make_data(time):
    def convert_value(item, value):
        if item == 'time':
            return log.time_string2datetime(value)
        if item == 'rain_flag':
            if float(value) == 0:
                return False
            else:
                return True
        if item == 'air_pressure' \
           or item == 'humidity1' \
           or item == 'humidity2':
            return int(round_float(float(value), 0))
        if item == 'wind_direction':
            return w.wind_direction2octas(float(value))
        return round_float(float(value), 0.1)

    log_lines = get_log_lines(time)
    return [{
        item: convert_value(item, value)
        for (item, value) in zip(w.data_keywords(), line.split())
    } for line in log_lines]

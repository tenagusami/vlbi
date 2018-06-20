import datetime as d
from decimal import Decimal, ROUND_HALF_UP
import tempfile
from functools import reduce
from openpyxl import Workbook
import asyncio


def utc_timezone():
    return d.timezone(d.timedelta(0))


def tmp_dir():
    return tempfile.gettempdir()


def increment_day(day):
    return day + d.timedelta(days=1)


def decrement_day(day):
    return day + d.timedelta(days=-1)


def round_float(r, order):
    rounded = Decimal(float(r)).quantize(
        Decimal(str(order)), rounding=ROUND_HALF_UP)
    if order > 0.1:
        return int(rounded)
    return float(rounded)


def doy2datetime(year, doy):
    return doy_string2datetime(str(year)+str(doy))


def doy_string2datetime(doy_string):
    date_tmp = d.datetime.strptime(doy_string + '+0000', '%Y%j%z')
    return datetime_at_0h(datetime2UTC(date_tmp))


def datetime2year_doy_string(today):
    return today.strftime('%Y'), today.strftime('%j')


def datetime2year_doy(today):
    return today.year, int(today.strftime('%j'))


def datetime2doy_string(today):
    year, doy = datetime2year_doy_string(today)
    return year + doy


def datetime2doy(today):
    return int(today.strftime('%j'))


def string_lines2string(string_lines):
    return reduce(lambda ss, s: ss + s + '\n', string_lines, '')


def get_now():
    date_tmp = d.datetime.now(d.timezone.utc)
    return datetime2UTC(date_tmp)


def is_offset_naive_datetime(datetime_obj):
    return not datetime_obj.tzinfo


def datetime2UTC(date_tmp):
    if date_tmp.tzinfo != d.timezone.utc:
        return date_tmp.astimezone(d.timezone.utc)
    return date_tmp


def datetime_at_0h(date_tmp):
    return d.datetime(
        date_tmp.year, date_tmp.month, date_tmp.day, tzinfo=date_tmp.tzinfo)


def make_out_data_matrix(title_row, in_data_matrix):
    out_matrix = [[row[item] for item in title_row] for row in in_data_matrix]
    out_matrix.insert(0, title_row)
    return out_matrix


def excel_file_out(file_path, sheet_title, data_matrix):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_title
    for data_row in data_matrix:
        ws.append(data_row)
    wb.save(file_path)


def async_execution(tasks):
    loop = asyncio.get_event_loop()
    future = asyncio.gather(*tasks)
    loop.run_until_complete(future)
    return future.result()

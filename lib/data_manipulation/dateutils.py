import datetime
import string

# Not that we expect that number of days in the week changes any time soon
# but having symbolic name in the source code is more descriptive and easier to search

DAYS_IN_WEEK = 7
MONTHS_IN_YEAR = 12

DAYS_IN_NON_LEAP_YEAR = 365
DAYS_IN_LEAP_YEAR = 366

_datetime_format_strings = dict({
    'dd-LLL-dddd dd:dd:dd': '%d-%b-%Y %H:%M:%S',
    'dd-LLL-dddd': '%d-%b-%Y',
    'd-LLL-dddd': '%d-%b-%Y',

    'dd/dd/dd': '%m/%d/%y',
    'd/dd/dd': '%m/%d/%y',
    'dd/d/dd': '%m/%d/%y',
    'd/d/dd': '%m/%d/%y',

    'dd/dd/dddd': '%m/%d/%Y',
    'dd/d/dddd': '%m/%d/%Y',
    'd/dd/dddd': '%m/%d/%Y',
    'd/d/dddd': '%m/%d/%Y',

    'dddd-LLL-dd': '%Y-%b-%d',
    'dddd-LLL-d': '%Y-%b-%d',

    'dd-LLL-dd': '%d-%b-%y',
    'd-LLL-dd': '%d-%b-%y',

    'dddd-dd-dd': '%Y-%m-%d',
    'dddd-dd-d': '%Y-%m-%d',
    'dddd-d-dd': '%Y-%m-%d',
    'dddd-d-d': '%Y-%m-%d',

    'dd.dd.dddd': '%d.%m.%Y',
    'd.dd.dddd': '%d.%m.%Y',
    'dd.d.dddd': '%d.%m.%Y',
    'd.d.dddd': '%d.%m.%Y',

    "d LLL dddd": '%d %b %Y',
    "dd LLL dddd": '%d %b %Y',
    "dLLLdddd": '%d%b%Y',
    "ddLLLdddd": '%d%b%Y',
    "dddddddd": '%Y%m%d'
})


def sniff_datetime_format(dtstr):
    """ Try to recognize date representation format from the date string
    """
    dtstr = dtstr.lower()
    ttab = string.maketrans(
        "0123456789abcdefghijklmnopqrstuvwxyz", "ddddddddddLLLLLLLLLLLLLLLLLLLLLLLLLL")
    fmtstring = dtstr.translate(ttab)
    if fmtstring in _datetime_format_strings:
        return _datetime_format_strings[fmtstring]
    else:
        raise ValueError("Incorrect date format string: %s" % fmtstring)


def asdatetime(dt):
    """ Extract datetime from several possible representations
    """
    if isinstance(dt, str):
        return datetime.datetime.strptime(dt, sniff_datetime_format(dt))
    elif isinstance(dt, datetime.date):
        return datetime.datetime(dt.year, dt.month, dt.day)
    else:
        raise ValueError("Cannot extract date from: %s" % repr(dt))


def asyear(dt):
    """ Extract year value from integer, date string, datetime.date or datetime.datetime class
    """
    if isinstance(dt, int):
        return dt
    elif isinstance(dt, datetime.date) or isinstance(dt, datetime.datetime):
        return dt.year
    elif isinstance(dt, str):
        dt = asdatetime(dt)
        return dt.year
    else:
        raise ValueError('Cannot extract year value from %s', repr(dt))


def leapyear(dt):
    """ Check if year is a leap year
    """
    yr = asyear(dt)
    if yr <= 1752:
        return yr % 4 == 0
    else:
        return (yr % 4 == 0) and (yr % 100 != 0 or yr % 400 == 0)


def yeardays(dt):
    if leapyear(dt):
        return DAYS_IN_LEAP_YEAR
    else:
        return DAYS_IN_NON_LEAP_YEAR


_days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_days_in_month_so_far = [0, 0, 31, 59, 90,
                         120, 151, 181, 212, 243, 273, 304, 334]


def eom(year, month):
    if month == 2 and leapyear(year):
        d = 29
    else:
        d = _days_in_month[month]
    return datetime.datetime(year, month, d)


def iseom(dt):
    """ Check if date is end of the month
    """
    dt = asdatetime(dt)
    return eom(dt.year, dt.month) == dt


def lweekday(year, month, weekday):
    """ Date of the last occurrence of weekday in month of a given year
    """
    last_day = eom(year, month)
    last_weekday = last_day.weekday()
    return last_day - datetime.timedelta(days=(last_weekday-weekday) % DAYS_IN_WEEK)


def nweekday(year, month, nth, weekday):
    """ Date of the n-th occurrence of weekday in month
    """
    first_weekday_of_month = datetime.datetime(year, month, 1).weekday()
    last_weekday_of_month = eom(year, month)
    day = 1+(weekday - first_weekday_of_month) % DAYS_IN_WEEK + \
        (nth-1)*DAYS_IN_WEEK
    if day > last_weekday_of_month.day:
        raise ValueError("No such n-th weekday in this month")
    return datetime.datetime(year, month, day)

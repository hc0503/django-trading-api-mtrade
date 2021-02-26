import datetime

from lib.data_manipulation import dateutils

_dc_norm = dict({
    '30/360 US': '30/360 US',
    '30U/360': '30/360 US',
    '360/360': '30/360 US',
    'BOND BASIS': '30/360 US',

    '30E/360': '30E/360',
    '30/360 ICMA': '30E/360',
    '30S/360 ICMA': '30E/360',
    'EUROBOND BASIS (ISDA 2006)': '30E/360',
    'SPECIAL GERMAN': '30E/360',

    '30E/360 ISDA': '30E/360 ISDA',
    'EUROBOND BASIS (ISDA 2000)': '30E/360 ISDA',
    'GERMAN': '30E/360 ISDA',

    '30E+/360': '30E+/360',



    'ACTUAL/ACTUAL ISDA': 'ACTUAL/ACTUAL ISDA',
    'ACTUAL/365': 'ACTUAL/ACTUAL ISDA',
    'ACT/365': 'ACTUAL/ACTUAL ISDA',
    'ACT/ACT': 'ACTUAL/ACTUAL ISDA',
    'ACTUAL/ACTUAL': 'ACTUAL/ACTUAL ISDA',

    'ACTUAL/365 FIXED': 'ACTUAL/365 FIXED',
    'ACT/365 FIXED': 'ACTUAL/365 FIXED',
    'A/365F': 'ACTUAL/365 FIXED',
    'ENGLISH': 'ACTUAL/365 FIXED',

    'ACTUAL/360': 'ACTUAL/360',
    'A/360': 'ACTUAL/360',
    'ACT/360': 'ACTUAL/360',
    'FRENCH': 'ACTUAL/360',

    'ACTUAL/365L': 'ACTUAL/365L',
    'ISMA-YEAR': 'ACTUAL/365L',

    'ACTUAL/ACTUAL AFB': 'ACTUAL/ACTUAL AFB',
    'ACT/ACT AFB': 'ACTUAL/ACTUAL AFB'
})


def _normalize_daycount_convention(convention):
    convention = convention.upper()
    return _dc_norm[convention]


def _period_has_29feb(dt1, dt2):
    have_29_feb = False
    y1 = dt1.year
    y2 = dt2.year
    for y in range(y1, y2+1):
        if dateutils.leapyear(y) and (
            (y != y1 and y != y2)
            or (y == y1 and dt1 < datetime.datetime(y1, 2, 29))
                or (y == y2 and datetime.datetime(y2, 2, 29) <= dt2)):
            have_29_feb = True
    return have_29_feb


def _daycount_parameters(dt1, dt2, convention, **kwargs):
    """ Return number of days and total number of days (i.e. numerator and
        denominator in the counting of year fraction between dates
    """
    convention = convention.upper()
    convention = _normalize_daycount_convention(convention)
    dt1 = dateutils.asdatetime(dt1)
    dt2 = dateutils.asdatetime(dt2)
    y1, m1, d1 = dt1.year, dt1.month, dt1.day
    y2, m2, d2 = dt2.year, dt2.month, dt2.day
    factor = None

    if convention in {'30/360 US', '30E/360', '30E/360 ISDA', '30E+/360'}:
        eom = 'eom' in kwargs and kwargs['eom']

        if convention == '30/360 US':
            # US adjustments
            if eom and dt1.month == 2 and dateutils.iseom(dt1) and dt2.month == 2 and dateutils.iseom(dt2):
                d2 = 30
            if eom and dt1.month == 2 and dateutils.iseom(dt1):
                d1 = 30
            if d2 == 31 and d1 >= 30:
                d2 = 30
            if d1 == 31:
                d1 = 30
        elif convention == '30E/360':
            if d1 == 31:
                d1 = 30
            if d2 == 31:
                d2 = 30
        elif convention == '30E/360 ISDA':
            if dateutils.iseom(dt1):
                d1 = 30
            if dateutils.iseom(dt2) and m2 != 2:
                d2 = 30
        elif convention == '30E+/360':
            if d1 == 31:
                d1 = 30
            if d2 == 31:
                m2 += 1
                if m2 == 13:
                    m2 = 1
                    y2 += 1
                d2 = 1

        num_days = (360*(y2-y1)+30*(m2-m1)+(d2-d1))
        year_days = 360

    elif convention == 'ACTUAL/ACTUAL ISDA':
        num_days = 0
        year_days = 0

        if y2 == y1:
            num_days = (dt2 - dt1).days
            year_days = dateutils.yeardays(y1)
        else:
            # we need to calculate factor properly
            factor = 0.0
            # full years between y1 and y2 exclusive
            for y in range(y1+1, y2):
                yd = dateutils.yeardays(y)
                num_days += yd
                year_days += yd
                factor += float(num_days)/year_days
            # days in the remaining part of the first year
            num = (datetime.datetime(y1+1, 1, 1) - dt1).days
            den = dateutils.yeardays(y1)
            num_days += num
            year_days += den
            factor += float(num)/den
            # days in the beginning of the last year
            num = (dt2 - datetime.datetime(y2, 1, 1)).days
            den = dateutils.yeardays(y2)
            num_days += num
            year_days += den
            factor += float(num)/den

    elif convention == 'ACTUAL/365 FIXED':
        num_days = (dt2-dt1).days
        year_days = 365
    elif convention == 'ACTUAL/360':
        num_days = (dt2-dt1).days
        year_days = 360
    elif convention == 'ACTUAL/365L':
        yearly_frequency = 'frequency' in kwargs and kwargs['frequency'] == 'yearly'
        if yearly_frequency:
            year_days = 366 if _period_has_29feb(dt1, dt2) else 365
        else:
            year_days = 366 if dateutils.leapyear(dt2) else 365
        num_days = (dt2-dt1).days
    elif convention == 'ACTUAL/ACTUAL AFB':
        year_days = 366 if _period_has_29feb(dt1, dt2) else 365
        num_days = (dt2-dt1).days
    else:
        raise ValueError('Unknown daycount convention \'%s\'' % convention)

    if factor is None:
        factor = float(num_days)/year_days

    return num_days, year_days, factor


def yearfrac(dt1, dt2, convention, **kwargs):
    """ Fractional number of years between two dates according to a given
        daycount convention
    """
    return _daycount_parameters(dt1, dt2, convention, **kwargs)[2]


def yearfractions(dates, convention, **kwargs):
    """ Convert dates to zero based float year value.

    Parameters
    ----------
    dates: list of datetime.date or datetime.datetime or strings representing dates
    convention: daycount convention

    Returns
    -------
    list of floats with 0.0 as the start corresponding to the first
    value in the list, all subsequent dates are converted to float year
    values by application of 'yearfrac' function.
    """
    if not dates:
        return []
    dts = map(dateutils.asdatetime, dates)
    return map(lambda x: yearfrac(dates[0], x, convention, **kwargs), dts)


def daydiff(dt1, dt2, convention, **kwargs):
    """ Calculate difference in days between tow days according to a given
        daycount convention
    """
    return _daycount_parameters(dt1, dt2, convention, **kwargs)[0]

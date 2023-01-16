import jdatetime


def getNextMonthStartNew(datetimeObject, georgian=False):
    if georgian:
        jalaliDateTime = jdatetime.datetime.fromgregorian(datetime=datetimeObject)
    else:
        jalaliDateTime = datetimeObject
    if jalaliDateTime.month <= 6:
        jalaliDateTime = jalaliDateTime + jdatetime.timedelta(days=31)
    else:
        jalaliDateTime = jalaliDateTime + jdatetime.timedelta(days=30)

    return jalaliDateTime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def monthLengthJalali(fromDate: str, toDate: str) -> dict:
    rangeDict = {}
    j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    year, month = list(map(int, fromDate.split('-')))
    fromDateJ = jdatetime.datetime(year=year, month=month, day=1)
    now = fromDateJ
    year, month = list(map(int, toDate.split('-')))
    toDateJ = jdatetime.datetime(year=year, month=month, day=1)
    while now <= toDateJ:
        year, month = now.year, now.month
        rangeDict[f"{year}-{month}"] = jdatetime.datetime(year=year, month=month, day=1).togregorian(), \
            jdatetime.datetime(year=year, month=month, day=j_days_in_month[month - 1],
                               hour=23, minute=59, second=59,
                               milliseconds=9999).togregorian()
        now = getNextMonthStartNew(now)
    return rangeDict


def fromDate_toDate():
    today = jdatetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    currentMonth = today.month
    currentYear = today.year
    todayStr = f"{currentYear}-{currentMonth}"
    date = monthLengthJalali(todayStr, todayStr)
    fromDate = None
    toDate = None
    for key, value in date.items():
        fromDate = value[0]
        toDate = value[1]

    return fromDate, toDate

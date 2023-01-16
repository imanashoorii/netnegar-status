from datetime import date
from datetime import datetime
import jdatetime as jdatetime
from status.enum import ServiceList


def toJalaliDateTime(d, time=True):
    if isinstance(d, date) and not isinstance(d, datetime):
        d = datetime(d.year, d.month, d.day)
    if d == None: return '-'
    try:
        if time == True:
            return jdatetime.datetime.fromgregorian(datetime=d).strftime("%Y/%m/%d-%H:%M:%S")
        else:
            return jdatetime.datetime.fromgregorian(datetime=d).strftime("%Y/%m/%d")
    except:
        return '-'


def getZoneName(zone):
    zones = {
        0: "Iran - Zirsakht",
        1: "Iran - Afranet",
        2: "Iran - Mobinnet",
        3: "Iran - Asiatech",
        4: "Iran - Soroush Rasaneh",
        5: "Iran - Parsonline",
        6: "Germany - Digital Ocean",
        7: "Netherlands - Digital Ocean",
        8: "USA - Digital Ocean"
    }
    for key, value in zones.items():
        if zone == key:
            zone = value
            return zone


def returnIranZones(zone):
    zones = {
        0: "Iran - Zirsakht",
        1: "Iran - Afranet",
        2: "Iran - Mobinnet",
        3: "Iran - Asiatech",
        4: "Iran - Soroush Rasaneh",
        5: "Iran - Parsonline",
    }
    for key, value in zones.items():
        if zone == key:
            zone = value
            return zone

def getServiceList():
    return [
        ServiceList.MONGODB,
        ServiceList.MYSQL,
        ServiceList.PANEL,
        ServiceList.API
    ]


def getIntervalList():
    return ["daily", "weekly", "monthly", "ninety"]


def convertIntervalToPersian(interval):
    zones = {
        "daily": "روزانه",
        "weekly": "هفتگی",
        "monthly": "ماهانه",
        "ninety": "سه ماهه",
    }
    for key, value in zones.items():
        if interval == key:
            interval = value
            return interval

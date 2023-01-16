from rest_framework import serializers
from datetime import datetime
import jdatetime
from .utils import toJalaliDateTime, getZoneName, convertIntervalToPersian
from math import ceil


class TimestampField(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):

        converted = datetime.fromtimestamp(float('%s' % data))
        return converted


class JalaliDateTimeField(serializers.Field):

    def to_representation(self, value):
        return toJalaliDateTime(value, time=True)

    def to_internal_value(self, data):
        return


class JalaliDateTimeFieldObject(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = datetime.strptime(data, "%Y-%m-%d")
            return toJalaliDateTime(data, time=False)
        return toJalaliDateTime(data, time=True)


class ConvertGregorianToJalaliDateOnly(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        fullDate = data.split("-")
        year = fullDate[0]
        month = fullDate[1]
        day = fullDate[2]
        return jdatetime.date.fromgregorian(day=int(year),month=int(month),year=int(day))


class ZoneConverter(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if data not in range(0, 9):
            raise serializers.ValidationError("مقدار zone صحیح نمیباشد")
        return getZoneName(data)

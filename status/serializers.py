from rest_framework_mongoengine import serializers
from .models import Incident
from .utils import toJalaliDateTime, getServiceList, getIntervalList
from .customFields import TimestampField, JalaliDateTimeField, ZoneConverter, JalaliDateTimeFieldObject
from rest_framework import serializers as DRFSerializer
from netnegar.models import HealthDetail
from math import ceil


class IncidentSerializer(serializers.DocumentSerializer):

    from_date = TimestampField()
    to_date = TimestampField()

    class Meta:
        model = Incident
        fields = ['title', 'from_date', 'to_date', 'signal', 'monitor', 'description', 'tags']

    def create(self, validated_data):
        incident = super().create(validated_data)
        incident.save()
        return incident

    def to_representation(self, instance: Incident):
        return {
            "title": instance.title,
            "from_date": toJalaliDateTime(instance.from_date),
            "to_date": toJalaliDateTime(instance.to_date),
            "signal": instance.signal,
            "monitor": instance.monitor,
            "description": instance.description,
            "tags": instance.tags,
            "createdAt": toJalaliDateTime(instance.updatedAt),
            "updatedAt": toJalaliDateTime(instance.updatedAt),
            "deletedAt": toJalaliDateTime(instance.deletedAt)
        }


class IncidentListSerializer(serializers.DocumentSerializer):
    from_date = JalaliDateTimeField(required=False)
    to_date = JalaliDateTimeField(required=False)

    class Meta:
        model = Incident
        fields = "__all__"

    def to_representation(self, instance: Incident):
        return {
            "title": instance.title,
            "from_date": toJalaliDateTime(instance.from_date),
            "to_date": toJalaliDateTime(instance.to_date),
            "signal": instance.signal,
            "monitor": instance.monitor,
            "description": instance.description,
            "tags": instance.tags,
            "createdAt": toJalaliDateTime(instance.createdAt),
            "updatedAt": toJalaliDateTime(instance.updatedAt),
            "deletedAt": toJalaliDateTime(instance.deletedAt)
        }


class HealthDetailSerializer(DRFSerializer.Serializer):
    service = DRFSerializer.CharField(required=True)
    zone = DRFSerializer.IntegerField(required=True)
    interval = DRFSerializer.CharField(required=True)

    def validate_service(self, service):
        if service not in getServiceList():
            raise DRFSerializer.ValidationError('سرویس وجود ندارد')
        return service

    def validate_interval(self, interval):
        if interval not in getIntervalList():
            raise DRFSerializer.ValidationError("مقدار interval صحیح نمیباشد")
        return interval

    def validate_zone(self, zone):
        if zone not in [0,1]:
            raise DRFSerializer.ValidationError("مقدار zone صحیح نمیباشد")
        return zone


class StatusBarSerializer(DRFSerializer.Serializer):
    service = DRFSerializer.CharField(required=True)
    zone = ZoneConverter(required=False)

    def validate_service(self, service):
        if service not in getServiceList():
            raise DRFSerializer.ValidationError('سرویس وجود ندارد')
        return service


class ChartSerializerData(DRFSerializer.Serializer):
    date = JalaliDateTimeFieldObject()
    percentile = DRFSerializer.IntegerField()
    interval = DRFSerializer.CharField()
    hour = DRFSerializer.IntegerField(required=False)




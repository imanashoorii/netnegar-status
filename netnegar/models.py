from django.db import models
import mongoengine_goodjson as gj
import mongoengine as db
from datetime import datetime
from mongoengine.queryset import (NotUniqueError, OperationError)
from mongoengine.errors import (InvalidDocumentError, SaveConditionError)


class HealthDetail(gj.Document):
    monitor = db.StringField(required=True)
    time = db.DateTimeField(required=True)
    value = db.IntField(required=True)
    trigger_type = db.IntField(required=True)
    zone = db.StringField(required=True)
    up = db.IntField(required=True)

    @classmethod
    def add_record(cls, data):
        try:
            cls(
                monitor=data.get("MonitorName"),
                time=datetime.now(),
                value=data.get("Value"),
                trigger_type=data.get("TriggerType"),
                zone=data.get("Zone"),
                up=data.get("Kind")
            ).save()
            return True
        except Exception:
            return False

    @classmethod
    def get_data(cls, **filters):
        try:
            data = cls.objects.filter(**filters)
            return data.to_mongo()
        except Exception:
            return False

    @staticmethod
    def data_process(filters):
        pass


class JsonBody(gj.Document):
    body = db.StringField()

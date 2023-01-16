from django.db import models
from django.contrib.auth.models import AbstractUser
import mongoengine_goodjson as gj
from mongoengine import *
from datetime import datetime


class User(AbstractUser):
    updatedAt = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.updatedAt = datetime.now()
        super(User, self).save(*args, **kwargs)


class Incident(gj.Document):
    title = StringField()
    from_date = DateTimeField()
    to_date = DateTimeField()
    signal = StringField()
    monitor = ListField()
    description = StringField()
    tags = ListField()
    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField()
    deletedAt = DateTimeField()

    meta = {
        'indexes': [
            {'fields': ['-title']},
            {'fields': ['-from_date']},
            {'fields': ['-to_date']},
            {'fields': ['-signal']},
            {'fields': ['-monitor']},
            {'fields': ['-description']},
            {'fields': ['-tags']},
        ]
    }

    def update(self, **kwargs):
        self.updatedAt = datetime.now()
        super(Incident, self).update(**kwargs)

    def delete(self, signal_kwargs=None, **write_concern):
        self.update(deletedAt=datetime.now())


class ErrorLog(gj.Document):
    time = DateTimeField()
    data = StringField(required=False)
    error = StringField()
    place = StringField(default=None)

    meta = {
        'indexes': [
            {'fields': ['-time']},
            {'fields': ['-data']},
            {'fields': ['-error']},
            {'fields': ['-place']}
        ]
    }

# -*- encoding=UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_str, smart_unicode
from django.conf import settings
import os
import re
import json
from datetime import date, datetime, timedelta
from django.template.defaultfilters import slugify

from django.db.models import Q
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse


# ---------------------------------------------
class Event(models.Model):
    title = models.CharField(max_length=500)
    venue = models.CharField(max_length=250)
    date = models.CharField(max_length=250)
    price = models.CharField(max_length=250, blank=True, null=True)
    events_overview = models.CharField(max_length=50000)
    tags = models.CharField(max_length=250)
# ------------------------------------------------


class Profile(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    timestamp_mod = models.DateTimeField(null=True, blank=True)

    pict = models.ImageField(upload_to='p1cture', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=250, null=True, blank=True)
    interested = models.ManyToManyField('SubTopic', blank=True)
    slug = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.user

class Storage(models.Model):
    TYPES = (
        ('filesystem', 'File System'),
        ('dropbox', 'Dropbox'),
        ('gdrive', 'Google Drive'),

    )
    parent = models.ForeignKey('Storage', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    bytes = models.FloatField(default=0)
    alternate_id = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=1000, null=True, blank=True)
    isDir = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    timestamp_mod = models.DateTimeField(null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    files = models.FileField(upload_to='upload')
    types = models.CharField(max_length=50, choices=TYPES, null=True, blank=True)
    ext = models.CharField(max_length=10, null=True, blank=True)

    token = models.CharField(max_length=100, null=True, blank=True)

    def kb(self):
        if self.bytes:
            return '%2.f' % (self.bytes / 1024)
        return 0

    def __unicode__(self):
        return '%s' % self.name

#class DropboxStorage(models.Model):



class Friend(models.Model):
    user = models.ManyToManyField(User)
    approved = models.BooleanField(default=False)

class Topic(models.Model):
    name = models.CharField(max_length=200)
    pict = models.ImageField(upload_to='p1cture', null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.name

class SubTopic(models.Model):
    topic = models.ForeignKey('Topic')
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s' % self.name


# Edure Middleware Handler
#
# Author: Hadi Wijaya (hadi.wijaya@voidsolution.com)

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, Template, RequestContext
from datetime import date, datetime, timedelta
from django.conf import settings
from django.contrib import auth

import getpass
import logging
import urllib
import os
import json
import requests
import commands

from edure.models import *
from datetime import date, timedelta
from django.middleware import csrf
from django.db import connection
from django.db import transaction

class DefaultMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            request.profile = Profile.objects.get(user=request.user)
        except Exception:
            pass

        try:
            request.storage = Storage.objects.filter(user=request.user)
        except Exception:
            pass
        try:
            request.storage_dropbox = Storage.objects.filter(user=request.user, types='dropbox')
        except Exception:
            pass

    def process_request(self, request):
        pass

# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render_to_response ,render
from django.template import Context, Template, RequestContext
from django.template import Template as template_django
from django.core import serializers
from django.core import urlresolvers
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.contrib import auth
from django.core import files
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode
from django.contrib.auth.decorators import login_required
from django import forms
from django.db.models import Q
from hashids import Hashids
from dateutil.relativedelta import relativedelta
from restclient import GET, POST, PUT, DELETE
from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage

import requests
import tempfile
import cStringIO
import urllib2
import re
import string
import pycountry
import os
import commands
import json
import whois
import uuid
import urllib2
import urllib
import string
import calendar
import logging
import random
import base64
import hashlib
import hmac
import time as times
import geocoder

from captcha.fields import CaptchaField
from datetime import date, datetime, timedelta, time
from django.utils.timezone import utc
from service.tasks import email_send
from edure.models import *


log = logging.getLogger("taaruf")
log.setLevel(logging.DEBUG)


class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

def login(request):
    if request.POST:
        try:
            email = request.POST.get('username')
            password = request.POST.get('password')
            if not User.objects.filter(username=email):
                if User.objects.filter(email=email):
                    email = User.objects.filter(email=email)[0].username
                elif Profile.objects.filter(phone=email):
                    email = Profile.objects.filter(phone=email)[0].user.username
                else:
                    raise Exception('User not found')

            cek_auth = auth.authenticate(username=email, password=password)
            auth.login(request, cek_auth)
        except Exception, err:
            request.session['err'] = str(err)
        else:
            return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile(request):
    if request.session.has_key('err'):
        err = request.session.get('err')
        del request.session['err']
    if request.session.has_key('success'):
        success = request.session.get('success')
        del request.session['success']

    if request.POST:
        try:
            pict = request.FILES.get('pict')
            fullname = request.POST.get('fullname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            birthday = request.POST.get('birthday')

            u = request.user
            u.email = email
            u.first_name = fullname
            u.username = username
            u.save()
            p = Profile.objects.get(user=u)
            p.phone = phone
            p.gender = gender
            p.birthday = datetime.strptime(birthday, '%d/%m/%Y').date()
            if pict:
                p.pict = pict
            p.save()
        except Exception, err:
            request.session['err'] = str(err)
        else:
            request.session['success'] = True
        return HttpResponseRedirect(reverse('profile'))

    return render_to_response('profile.html', locals(), context_instance=RequestContext(request))

def handle_page_not_found_404(request):
    return HttpResponseRedirect(reverse('dashboard'))

def word_processing(request, key=None):
    if key:
        s = Storage.objects.get(user=request.user, token=key)
        return render_to_response('word_processing.html', locals(), context_instance=RequestContext(request))
    else:
        filename = request.POST.get('filename')
        types = request.POST.get('type')
        token = uuid.uuid1().hex
        try:
            try:
                s = Storage.objects.get(user=request.user, token=key)
            except Exception:
                s = Storage()
            s.name = filename
            s.token = token
            s.user = request.user
            s.timestamp_mod = datetime.now()
            try:
                parent = Storage.objects.get(id=request.POST.get('parent'))
            except Exception:
                parent = None
            if parent:
                s.parent = parent
            s.bytes = 0
            s.ext = types
            s.isDir = False
            s.types = 'filesystem'
            s.save()
        except Exception, err:
            return HttpResponse(str(err))
        else:
            return HttpResponseRedirect(reverse('word_processing', kwargs={'key':s.token}))
    return render_to_response('word_processing.html', locals(), context_instance=RequestContext(request))

def onlyoffice(request):
    key = 'JkJhsSK98341'
    return render_to_response('onlyoffice.html', locals(), context_instance=RequestContext(request))

@login_required
def dashboard(request):
    if request.session.has_key('err') or request.session.has_key('success'):
        err = request.session.get('err')
        success = request.session.get('success')
        if request.session.has_key('err'):
            del request.session['err']
        if request.session.has_key('success'):
            del request.session['success']

    try:
        link_data = Link.objects.filter(user=request.user, hidden=False)
    except Exception:
        pass
    return render_to_response('app/main.html', locals(), context_instance=RequestContext(request))


def home(request, slug=None):
    if slug:
        try:
            p = Profile.objects.get(slug=slug)
        except Exception:
            pass
        else:
            return render_to_response('dashboard.html', locals(), context_instance=RequestContext(request))
    if not request.user.is_authenticated():
        return register(request)
    return render_to_response('main.html', locals(), context_instance=RequestContext(request))

@login_required
def storage(request):

    if request.POST.get('filename') and request.POST.get('id'):
        try:
            s = Storage.objects.get(user=request.user, id=request.POST.get('id'))
            s.name = request.POST.get('filename')
            s.timestamp_mod = datetime.now()
            s.save()
        except Exception, err:
            resp = {'status': False, 'msg': unicode(err)}
        else:
            resp = {'status': True}

        return HttpResponse(json.dumps(resp), content_type='application/json')

    if request.POST.get('delete_file'):
        try:
            Storage.objects.get(user=request.user, id=request.POST.get('delete_file')).delete()
        except Exception, err:
            resp = {'status': False, 'msg': unicode(err)}
        else:
            resp = {'status': True}

        return HttpResponse(json.dumps(resp), content_type='application/json')

    if request.POST.get('folder_name'):
        try:
            try:
                s = Storage.objects.get(user=request.user, name=request.POST.get('folder_name'))
            except Exception:
                s = Storage()
            s.name = request.POST.get('folder_name')
            s.user = request.user
            s.timestamp_mod = datetime.now()
            try:
                parent = Storage.objects.get(id=request.POST.get('parent'))
            except Exception:
                parent = None
            if parent:
                s.parent = parent
            s.bytes = 0
            s.isDir = True
            if request.POST.get('type') == 'dropbox':
                s.types = 'dropbox'
            if request.POST.get('type') == 'drive':
                s.types = 'gdrive'
            if request.POST.get('type') == 'library':
                s.types = 'filesystem'
            s.save()
        except Exception, err:
            resp = {'status': False, 'msg': unicode(err)}
        else:
            resp = {'status': True}

        return HttpResponse(json.dumps(resp), content_type='application/json')

# dropbox store files
    if request.POST.get('raw_json'):
        try:
            raw_json = json.loads(request.POST.get('raw_json'))

    # {"isDir":false,"name":"Get Started with Dropbox Paper.url","bytes":81,"link":"https://www.dropbox.com/s/h6e130jd6av9y4f/Get%20Started%20with%20Dropbox%20Paper.url?dl=0","accountId":"dbid:AABASMXaCO-WHojq4kFiEr0KFJejGkWkR1I","id":"id:U5PPO8balnAAAAAAAAAABg","icon":"https://www.dropbox.com/static/images/icons64/page_white_linkfile.png"}
            for i in raw_json:
                try:
                    s = Storage.objects.get(user=request.user, link=link)
                except Exception:
                    s = Storage()
                s.name = i['name']
                s.user = request.user
                s.timestamp_mod = datetime.now()
                try:
                    parent = Storage.objects.get(id=request.POST.get('parent'))
                except Exception:
                    parent = None
                if parent:
                    s.parent = parent

                s.link = i['link']
                s.bytes = i['bytes']
                s.icon = i['icon']
                s.isDir = i['isDir']
                s.alternate_id = i['id']
                s.types = 'dropbox'
                s.save()
        except Exception, err:
            resp = {'status': False, 'msg': unicode(err)}
        else:
            resp = {'status': True}
        return HttpResponse(json.dumps(resp), content_type='application/json')

# library store file
    if request.FILES.get('file_library'):
        try:
            file_library = request.FILES.get('file_library')
            try:
                s = Storage.objects.get(user=request.user, name=file_library.name)
            except Exception:
                s = Storage()
            s.name = file_library.name
            s.user = request.user
            s.timestamp_mod = datetime.now()
            try:
                parent = Storage.objects.get(id=request.POST.get('parent'))
            except Exception:
                parent = None
            if parent:
                s.parent = parent

            s.files = file_library
            s.bytes = file_library.size
            s.isDir = False
            s.types = 'filesystem'
            s.save()
        except Exception, err:
            resp = {'status': False, 'msg': unicode(err)}
        else:
            resp = {'status': True}
            if not parent:
                return HttpResponseRedirect(reverse('file_manager_library'))
            return HttpResponseRedirect(reverse('file_manager_library', kwargs={'key':parent.id}))

    return HttpResponse('')

@login_required
def file_manager(request):
    return HttpResponseRedirect(reverse('file_manager_library'))

@login_required
def file_manager_library(request, key=None):
    def get_parent(p, result=[]):
        result.append(p)
        if p.parent:
            return get_parent(p.parent, result)
        return result

    file_manager_title = 'Library'
    parent = None
    if key:
        parent = Storage.objects.get(id=key)
        file_list = Storage.objects.filter(user=request.user, parent=parent, types='filesystem').order_by('-id')
    else:
        file_list = Storage.objects.filter(user=request.user, parent=None, types='filesystem').order_by('-id')

    if parent:
        breadcumb = get_parent(parent)
        breadcumb.reverse()
        breadcumb_link = '<a href="%s">Library</a>' % reverse('file_manager_library')
        for i in breadcumb:
            breadcumb_link += '/<a href="%s">%s</a>' % (reverse('file_manager_library', kwargs={'key':i.id}), i.name)
        breadcumb = breadcumb_link
    return render_to_response('file_manager.html', locals(), context_instance=RequestContext(request))

@login_required
def file_manager_drive(request, key=None):
    def get_parent(p, result=[]):
        result.append(p)
        if p.parent:
            return get_parent(p.parent, result)
        return result

    file_manager_title = 'Google Drive'
    parent = None
    if key:
        parent = Storage.objects.get(id=key)
        file_list = Storage.objects.filter(user=request.user, parent=parent, types='gdrive').order_by('-id')
    else:
        file_list = Storage.objects.filter(user=request.user, parent=None, types='gdrive').order_by('-id')

    if parent:
        breadcumb = get_parent(parent)
        breadcumb.reverse()
        breadcumb_link = '<a href="%s">Google Drive</a>' % reverse('file_manager_drive')
        for i in breadcumb:
            breadcumb_link += '/<a href="%s">%s</a>' % (reverse('file_manager_drive', kwargs={'key':i.id}), i.name)
        breadcumb = breadcumb_link
    return render_to_response('file_manager.html', locals(), context_instance=RequestContext(request))

@login_required
def file_manager_dropbox(request, key=None):
    def get_parent(p, result=[]):
        result.append(p)
        if p.parent:
            return get_parent(p.parent, result)
        return result

    file_manager_title = 'Dropbox'
    parent = None
    if key:
        parent = Storage.objects.get(id=key)
        file_list = Storage.objects.filter(user=request.user, parent=parent, types='dropbox').order_by('-id')
    else:
        file_list = Storage.objects.filter(user=request.user, parent=None, types='dropbox').order_by('-id')

    if parent:
        breadcumb = get_parent(parent)
        breadcumb.reverse()
        breadcumb_link = '<a href="%s">Dropbox</a>' % reverse('file_manager_dropbox')
        for i in breadcumb:
            breadcumb_link += '/<a href="%s">%s</a>' % (reverse('file_manager_dropbox', kwargs={'key':i.id}), i.name)
        breadcumb = breadcumb_link
    return render_to_response('file_manager.html', locals(), context_instance=RequestContext(request))


@login_required
def info_tech(request):
    return render_to_response('info_tech.html', locals(), context_instance=RequestContext(request))

@login_required
def physics(request):
    return render_to_response('physics.html', locals(), context_instance=RequestContext(request))

@login_required
def computer(request):
    return render_to_response('computer.html', locals(), context_instance=RequestContext(request))

@login_required
def friend_lists(request):
    return render_to_response('friend_lists.html', locals(), context_instance=RequestContext(request))

@login_required
def sports(request):
    return render_to_response('sports.html', locals(), context_instance=RequestContext(request))

@login_required
def events(request):
    all_events = Event.objects.all()
    context ={
        'all_events' : all_events,
    }
    # return render_to_response('events.html', context, context_instance = RequestContext(request))
    return render(request, 'events.html', context)

@login_required
def on_this_day(request):
    return render_to_response('on_this_day.html', locals(),  context_instance=RequestContext(request))

@csrf_exempt
def register(request):
    if request.session.has_key('err'):
        err = request.session.get('err')
        del request.session['err']

    if request.POST:
        try:
            fullname = request.POST.get('fullname')
            username = request.POST.get('username_reg')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password_reg')
            gender = request.POST.get('gender')
            birthday = request.POST.get('birthday')
            if fullname and username and email and password and gender and birthday and phone:
                if not re.match(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$', email):
                    raise Exception('Invalid Email Format')
                        #return HttpResponseRedirect(reverse('register'))
                        #return HttpResponse(json.dumps(resp), content_type='application/json')

                if User.objects.filter(username=username):
                    raise Exception('This username is already exist')
                if User.objects.filter(email=email):
                    raise Exception('This email is already exist')
                if phone and Profile.objects.filter(phone=phone):
                    raise Exception('This phone is already exist')
                u = User.objects.create_user(username=username, email=email, password=password)
                u.is_staff = False
                u.is_superuser = False
                u.first_name = fullname
                u.save()

                p = Profile()
                p.user = u
                p.timestamp_mod = datetime.now()
                p.gender = gender
                p.birthday = datetime.strptime(birthday, '%d/%m/%Y').date()
                p.phone = phone
                p.save()
        except Exception, err:
            request.session['err'] = str(err)
            #resp = {'status': False, 'msg': unicode(err)}
        else:
            cek_auth = auth.authenticate(username=username, password=password)
            auth.login(request, cek_auth)
            key = uuid.uuid1().hex

            #v = Verification()
            #v.user = u
            #v.key = key
            #v.save()
            #save key to models
            if not phone:
                subject = 'EduRe email verification'
                msg = '''
    <p>Please click link below for verification process</p>
    <p><a href="http://%s/activation/%s" target="_blank">http://%s/activation/%s</a></p>
                    ''' % (request.META.get('HTTP_HOST'), key, request.META.get('HTTP_HOST'), key)
                email_send.delay(subject, email, msg, fr=settings.ADMIN_EMAIL, title='EduRe')
            return HttpResponseRedirect(reverse('home'))

            #send_sms_task.delay(settings.ADMIN_PHONE, text)
        err = request.session['err']
        del request.session['err']
    return render_to_response('register.html', locals(), context_instance=RequestContext(request))

def get_captcha(request):
    try:
        form = template_django(CaptchaTestForm())
        form = form.render(Context())
    except Exception, err:
        return HttpResponse(err)
    else:
        log.debug('CAPTCHA content: %s' % form)
    return HttpResponse(form)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))

def activation(request, key):
    try:
        v = Verification.objects.get(key=key)
    except Exception, err:
        return HttpResponseRedirect(reverse('home'))
    v.verified = True
    v.save()
    return render_to_response('app/activation.html', locals(), context_instance=RequestContext(request))

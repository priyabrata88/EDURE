#!/bin/bash

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
dpkg-reconfigure locales

apt-get update
apt-get install python mercurial python-dev python-pip mysql-server mysql-client libmysqlclient-dev python-imaging libxml2-dev libxslt1-dev gcc python-dev tk8.5 tcl8.5 tk8.5-dev tcl8.5-dev nginx gunicorn
apt-get build-dep python-imaging --fix-missing
pip install virtualenv
pip install uwsgi
pip install --upgrade pip

virtualenv ../TRACKLINK
source ../TRACKLINK/bin/activate
apt-get install libjpeg8-dev
ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib

pip install -r requirements.txt

mysql -uroot -e "create database tracklink; create user tracklink identified by 'tracklink'; grant all privileges on * . * to tracklink;" -p

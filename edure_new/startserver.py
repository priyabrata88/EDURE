#!/usr/bin/python
import subprocess
import sys
import os
import commands
import re
import time


try:
    if sys.argv[1] == 'kill':
        for i in commands.getoutput('ps -ax | grep gunicorn').split('\n'):
            if re.search('/home/ubuntu/ngepet_env/bin/python /home/ubuntu/ngepet_env/bin/gunicorn --workers 3', i):
                if re.search(r'([0-9]+) ', i):
                    os.kill(int(re.search(r'([0-9]+) ', i).groups()[0]), 9)
                    print 'kill: %s' % re.search(r'([0-9]+) ', i).groups()[0]
        for i in commands.getoutput('ps -ax | grep daphne').split('\n'):
            if re.search('/home/ubuntu/ngepet_env/bin/python /home/ubuntu/ngepet_env/bin/daphne -e ssl:8888:privateKey=/etc/letsencrypt/live/bitroll.net/privkey.pem:certKey=/etc/letsencrypt/live/bitroll.net/fullchain.pem', i):
                if re.search(r'([0-9]+) ', i):
                    os.kill(int(re.search(r'([0-9]+) ', i).groups()[0]), 9)
                    print 'kill: %s' % re.search(r'([0-9]+) ', i).groups()[0]
        for i in commands.getoutput('ps -ax | grep runworker').split('\n'):
            if re.search('python manage.py runworker --threads 2', i):
                if re.search(r'([0-9]+) ', i):
                    os.kill(int(re.search(r'([0-9]+) ', i).groups()[0]), 9)
                    print 'kill: %s' % re.search(r'([0-9]+) ', i).groups()[0]
        for i in commands.getoutput('ps -ax | grep rate.py').split('\n'):
            if re.search('python rate.py', i):
                if re.search(r'([0-9]+) ', i):
                    os.kill(int(re.search(r'([0-9]+) ', i).groups()[0]), 9)
                    print 'kill: %s' % re.search(r'([0-9]+) ', i).groups()[0]

except Exception:
    subprocess.Popen(['nohup', '/home/ubuntu/ngepet_env/bin/python', '/home/ubuntu/ngepet_env/bin/gunicorn', '--workers', '3', '--bind', 'unix:/home/ubuntu/ngepet/ngepet.sock', 'ngepet.wsgi:application', '&'])
    time.sleep(2)
    subprocess.Popen(['nohup', '/home/ubuntu/ngepet_env/bin/daphne', '-e', 'ssl:8888:privateKey=/etc/letsencrypt/live/bitroll.net/privkey.pem:certKey=/etc/letsencrypt/live/bitroll.net/fullchain.pem', '-b', '0.0.0.0', 'ngepet.asgi:channel_layer', '--port', '8888', '&'])
    time.sleep(2)
    subprocess.Popen(['nohup', '/home/ubuntu/ngepet_env/bin/python', 'manage.py', 'runworker', '--threads', '2', '&'])
    time.sleep(2)
    subprocess.Popen(['nohup', '/home/ubuntu/ngepet_env/bin/python', 'rate.py', '&'])

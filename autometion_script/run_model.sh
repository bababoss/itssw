#!/usr/bin/env bash
sleep 1

# object_detection api service
if screen -list | grep -q "rnpr"; then
   screen -X -S rnpr quit
fi

cd  /home/gpu-machine/projects/rnpd
path_api="cd /home/gpu-machine/projects/rnpd\n"
envn="workon vision3Env\n"
exp="export PYTHONPATH=`pwd`\n"
screen -dmS rnpr bash
screen -S rnpr -X stuff "$path_api python manage.py runserver 0.0.0.0:8890\n"
sleep 5

#!/usr/bin/env bash
sudo supervisorctl stop acc_apigateway_stage_celery
sleep 5
sudo supervisorctl stop acc_apigateway_stage_speech

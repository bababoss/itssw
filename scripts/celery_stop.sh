#!/usr/bin/env bash
sudo supervisorctl stop acc_apigateway_celery
sleep 5
sudo supervisorctl stop acc_apigateway_speech
sleep 2
sudo supervisorctl stop acc_apigateway_postprocess
sleep 2
sudo supervisorctl stop acc_apigateway_gpu

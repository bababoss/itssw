#!/usr/bin/env bash
sudo supervisorctl restart acc_apigateway_celery
sleep 5
sudo supervisorctl restart acc_apigateway_speech
sleep 5
sudo supervisorctl restart acc_apigateway_gpu
sleep 5
sudo supervisorctl restart acc_apigateway_postprocess

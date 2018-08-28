#!/usr/bin/env bash
sudo supervisorctl restart acc_apigateway_stage_celery
sleep 5
sudo supervisorctl restart acc_apigateway_stage_speech

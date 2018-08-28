"""
@Auther : Suresh
"""
import logmatic,time,os
import logging,socket
from django.conf import settings
BASE_DIR=settings.BASE_DIR


def access_log(logger,handler,log_file,log_data={}):
    log_data['hostname']=socket.gethostname()
    log_file=os.path.join(BASE_DIR,log_file)
    logHandler = handler.TimedRotatingFileHandler(log_file, when='H', interval=1, backupCount=0)
    logHandler.setFormatter(logmatic.JsonFormatter(extra=log_data))
    return logHandler


    

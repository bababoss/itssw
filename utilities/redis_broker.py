"""
@Copyright : Cogknit Semantics pvt limited
@Author :    Suresh Saini
@Email  :    suresh@cogknit.com
@Date    :   12th April 2018
"""
import os
import time
import traceback
from django_redis import get_redis_connection
from celery.task.control import inspect

class RedisBroker(object):
    """
    Redis broker class
    """
    def __init__(self):
        # connect to redis server
        self.redis_conn=get_redis_connection("default")
    def get_redis_connection(self):
        return self.redis_conn

    def redis_subscriber(self,channel='startScripts',msg='START'):
        try:

            PAUSE = True
            start_new_task=False
            st=time.time()
            while PAUSE:  # Will stay in loop until START message received
                
                message =  self.redis_conn.get(channel) # Checks for message
                print("Waiting for message " +str(message)+" key "+channel+" msg "+msg)
                if message:
                    if message == str.encode(msg):  # Checks for START message
                        PAUSE = False  # Breaks loop
                        print("Task is complete: "+channel+msg)
                        self.redis_conn.delete(channel)
                        start_new_task=True
                time.sleep(5)
                et=time.time()
                ttime=int(et-st)
                
                
                if ttime>=720000:
                    start_new_task=True
                    break
                    
            return start_new_task

        except Exception as e:
            print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
            print(str(e))
            print(traceback.format_exc())
            return False

    
    
    
    def subscriber(self,channel='startScripts',msg='START'):
        try:
            p = self.redis_conn.pubsub()  # See https://github.com/andymccurdy/redis-py/#publish--subscribe
            p.subscribe(channel)  # Subscribe to startScripts channel 'startScripts'
            PAUSE = True
            start_new_task=False
            st=time.time()
            while PAUSE:  # Will stay in loop until START message received
                
                message = p.get_message()  # Checks for message
                print("Waiting for "+channel+" msg "+msg)
                if message:
                    command = message['data']  # Get data from message
                    print("message_data:  ",command)
                    if command == str.encode(msg):  # Checks for START message
                        PAUSE = False  # Breaks loop
                        print("Task is complete: "+channel+msg)
                        start_new_task=True
                time.sleep(2)
                et=time.time()
                ttime=int(et-st)
                
                
                if ttime>=2700:
                    start_new_task=True
                    break
                    
            return start_new_task

        except Exception as e:
            print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
            print(str(e))
            print(traceback.format_exc())
            return False

        
        
    def subscriber_gpu(self,channel='startScripts',msg='START'):
        try:
            p = self.redis_conn.pubsub()  # See https://github.com/andymccurdy/redis-py/#publish--subscribe
            p.subscribe(channel)  # Subscribe to startScripts channel 'startScripts'
            PAUSE = True
            start_new_task=False
            st=time.time()
            while PAUSE:  # Will stay in loop until START message received
                
                message = p.get_message()  # Checks for message
                print("Waiting for "+channel+" msg "+msg)
                if message:
                    command = message['data']  # Get data from message
                    print("message_data:  ",command)
                    if command == str.encode(msg):  # Checks for START message
                        PAUSE = False  # Breaks loop
                        print("Task is complete: "+channel+msg)
                        start_new_task=True
                time.sleep(2)
                et=time.time()
                ttime=int(et-st)
                
                if ttime>=2700:
                    start_new_task=True
                    break
                    
            i=inspect()
            state=True
            while state:
                data=i.active()
                lenght=len(data['celery@worker_gpu'])
                state=True
                print("Waiting for empty gpu queue to "+channel+ " msg" +msg)
                time.sleep(5)
                if lenght<2:
                    state=False
                    break
            return start_new_task

        except Exception as e:
            print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
            print(str(e))
            print(traceback.format_exc())
            return False

        

    def publisher(self,channel='startScripts'):
        try:

            # HERE SOME INITIAL WORK IS DONE THAT SCRIPTS 1 & 2 NEED TO WAIT FOR
            # IDs SERIAL PORTS
            # SAVE TO db
            status=True
            if status:    
                self.redis_conn.publish(channel, 'START')  # PUBLISH START message on startScripts channe
                print(channel+" Task published")

        except Exception as e:
            print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
            print(str(e))
            print(traceback.format_exc())

if __name__=="__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'rnpd.settings'
    rb=RedisBroker()
    rb.publisher()

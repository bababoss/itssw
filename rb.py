"""
Auther : Suresh Saini
Email: suresh@cogknit@com
"""
import redis,os
import time
import traceback
from django_redis import get_redis_connection
class RedisBroker(object):
    def __init__(self):
        self.redis_conn=get_redis_connection("default")

    def subscriber(self):
        try:

            p = self.redis_conn.pubsub()  # See https://github.com/andymccurdy/redis-py/#publish--subscribe
            p.subscribe('startScripts')  # Subscribe to startScripts channel
            PAUSE = True
            while PAUSE:  # Will stay in loop until START message received
                print("Waiting For redisStarter...")
                message = p.get_message()  # Checks for message
                if message:
                    command = message['data']  # Get data from message
                    if command == b'START':  # Checks for START message
                        PAUSE = False  # Breaks loop

                time.sleep(1)

            print("Permission to start...")

        except Exception as e:
            print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
            print(str(e))
            print(traceback.format_exc())


    def publisher(self):
        try:

            # HERE SOME INITIAL WORK IS DONE THAT SCRIPTS 1 & 2 NEED TO WAIT FOR
            # IDs SERIAL PORTS
            # SAVE TO db

            print("Starting main scripts...")

            self.redis_conn.publish('startScripts', 'START')  # PUBLISH START message on startScripts channel

            print("Done")

        except Exception as e:
            print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
            print(str(e))
            print(traceback.format_exc())

if __name__=="__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'rnpd.settings'
    rb=RedisBroker()
    rb.publisher()


import os
from celery.schedules import crontab

class Config:
    DEBUG=True
    SECRET_KEY='6ab68d27e4d4a6fa2cdc05e963622a60'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME='iitmbhavesh@gmail.com'
    MAIL_PASSWORD='qxitpxtbhbxplkxe'
    MAIL_DEFAULT_SENDER='iitmbhavesh@gmail.com'
    JWT_COOKIE_SECURE=False
    JWT_TOKEN_LOCATION=["cookies"]
    JWT_SECRET_KEY='abcdovnspvovwonoesvnno239394c0e0edjd'
    JWT_ACCESS_TOKEN_EXPIRES=15
    JWT_REFRESH_TOKEN_EXPIRES=12
    SQLALCHEMY_DATABASE_URI='sqlite:///lms.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    OTP_SECRET_KEY='6ab68d27e4d4a6fa2cdc05e963622a60'
    CACHE_TYPE='RedisCache'
    CACHE_REDIS_HOST='localhost'
    CACHE_REDIS_PORT=6379
    CACHE_REDIS_DB=3
    CACHE_CONFIG_PREFIX=''
    CELERY_CONFIG={"broker_url":"redis://localhost:6379/1",
                   "result_backend":"redis://localhost:6379/2",
                   "result_expires":360,
                   "ignore_result":True,
                   "worker_concurrency":4,
                   "broker_connection_retry_on_startup":True,
                   "timezone":"Asia/Kolkata",
                   "beat_schedule":{
                       'send_reports': {
                           'task': 'lms.tasks.send_reports',
                           'schedule': crontab(day_of_month=1, hour=0, minute=0)   # 1st of every month 
                           # for demo:  crontab(minute="*/3")
                           },
                        'daily_reminders': {
                               'task': 'lms.tasks.daily_reminders',
                               'schedule': crontab(hour=19, minute=0)   # 7 PM daily 
                               # for demo: crontab(minute='*/6')
                            },
                        'delete_transactions':{
                            'task':'lms.tasks.delete_transactions',
                            'schedule': crontab(minute = '*/20')
                            # for demo: crontab(minute = '*/2')
                        }
                        
                    }
                }

    ROOT_PATH = os.getcwd()

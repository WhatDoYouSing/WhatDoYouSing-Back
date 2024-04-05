from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .views import update_non_user_recomlist


def start():
    scheduler=BackgroundScheduler()
    # scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    # register_events(scheduler)

    @scheduler.scheduled_job('cron', minute='*/10', second='0')
    def auto_check():
        update_non_user_recomlist()

    scheduler.start()

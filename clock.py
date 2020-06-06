from apscheduler.schedulers.blocking import BlockingScheduler
import test

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')
    test.main()

sched.start()

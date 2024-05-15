import os, time, json
from celery import Celery, Task
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

app = Celery('project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()




@app.task
def error_handler(request, exc, traceback):
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
          request.id, exc, traceback))
    print('=====  Error on the top =====')





@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')




@app.task(bind=True)
def hello(self, a, b):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(1)
    return 'hello world: %i' % (a+b)



class CustomTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3, 'countdown': 0.2}
    retry_backoff = True
    retry_jitter = True

@app.task(bind=True, base=CustomTask)
def addNum(self, x, y):
    try:
        result = x + y
        if result == 4:  # Intentionally causing an error for testing
            raise ValueError("Intentional Error")
        return result
    except Exception as exc:
        self.retry(exc=exc)
    



app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'app.tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
    'multiply-at-8-am': {
        'task': 'app.tasks.mul',
        'schedule': crontab(hour=8, minute=0),
        'args': (4, 5)
    },
    'sum-every-monday-morning': {
        'task': 'app.tasks.calculate',
        'schedule': crontab(hour=7, minute=30, day_of_week='monday'),
        'args': (10, 10)
    },
}




from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule

# Define the interval
try:
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )
except Exception:
    pass


# # Create the periodic task
# PeriodicTask.objects.create(
#     interval=schedule,  # we created this above
#     name='Add every 10 seconds',  # a unique name
#     task='app.tasks.add',  # name of task
#     args=json.dumps([10, 10]),  # JSON arguments
# )

# Create the periodic task
try:
    addtask, addcreate = PeriodicTask.objects.get_or_create(
            interval=schedule,  # we created this above
            name='Add every 10 seconds',  # a unique name
            task='app.tasks.add',  # name of task
            args=json.dumps([10, 10]),  # JSON arguments
            # args=(18, 973),  # JSON arguments
        )
    print('ok ')
    addtask.enabled = True
    addtask.save()
except Exception:
    pass




try:
    # Define the crontab schedule
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='8',
        day_of_week='mon',
        day_of_month='*',
        month_of_year='*',
    )
    schedule.enabled = True
except Exception:
    pass

try:
    # Create the periodic task
    mul_task, mul_create = PeriodicTask.objects.get_or_create(
        crontab=schedule,  # we created this above
        name='Multiply at 8am every Monday',  # a unique name
        task='app.tasks.mul',  # name of task
        args=json.dumps([4, 5]),  # JSON arguments
        # args=(84,848),  # JSON arguments
        )
    mul_task.save()
except Exception:
    pass
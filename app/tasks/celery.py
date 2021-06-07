import os

from celery import Celery


app = Celery('tasks', include=['tasks.tasks'],
             broker=os.environ.get('CELERY_BROKER'),
             backend=os.environ.get('CELERY_BACKEND'))

app.conf.beat_schedule = {
    "call_ms": {
        "task": "tasks.tasks.call_ms",
        "schedule": 60.0
    }
}


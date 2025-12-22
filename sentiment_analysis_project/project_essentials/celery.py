import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE","sent_analysis.settings")

app=Celery("sent_analysis")
app.config_from_object("django.conf:settings",namespace="CELERY")
app.conf.beat_schedule={
    "stream_and_save_per_minute":{
        "task":"sent_app.tasks.stream_and_save_comments",
        "schedule":crontab(minute="*/1"),
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"request:{self.request!r}")
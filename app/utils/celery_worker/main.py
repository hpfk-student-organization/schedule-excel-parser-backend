from app.utils.celery_worker.config import app
from celery import Task
from app.utils.celery_worker.sheduler_parser import SchedulerParser


class BaseTaskWithRetry(Task):
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True

@app.task(bind=True, base=BaseTaskWithRetry)
def task_manager(self, file_name):
    try:
        scheduler_parser = SchedulerParser()
        return scheduler_parser.run()
    except Exception as e:
        # Якщо виникла помилка, перезапустити завдання знову
        self.retry(exc=e, countdown=1, max_retries=3)
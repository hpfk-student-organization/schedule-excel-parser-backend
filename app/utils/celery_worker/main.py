import io

from app.utils.celery_worker.config import app
from celery import Task
from app.utils.celery_worker.sheduler_parser import SchedulerParser


class BaseTaskWithRetry(Task):
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@app.task(bind=True, base=BaseTaskWithRetry)
def task_manager(self, file_io):
    try:
        scheduler_parser = SchedulerParser(io.BytesIO(file_io))
        return 'Goodd'
    except Exception as e:
        # Якщо виникла помилка, перезапустити завдання знову
        self.retry(exc=e, countdown=1, max_retries=3)

from app.utils.requests.create_json import create_response, BaseResponse
from fastapi import APIRouter, UploadFile, Form, status
from fastapi.responses import JSONResponse

from app.utils.celery_worker.main import task_manager
from app.utils.celery_worker.config import app as celery_app

router = APIRouter()


class GetCeleryTasks:

    def __init__(self, task_id: str):
        self.task_id = task_id

    def exist_in_list(self, tasks: list):
        """Повертає номер задачі, або None"""
        for index, task in enumerate(tasks):
            if self.task_id == task['id']:
                return index

    def get_detail_task_in_queue(self, short_queue: list, long_queue: list):
        len_queue = len(short_queue) + len(long_queue)

        number_in_tasks = self.exist_in_list(short_queue)
        if number_in_tasks is not None:
            return {
                'number_in_tasks': number_in_tasks + 1,
                'type_queue': 'short',
                'len_queue': len_queue
            }

        number_in_tasks = self.exist_in_list(long_queue)
        if number_in_tasks is not None:
            return {
                'number_in_tasks': len(short_queue) + number_in_tasks + 1,
                'type_queue': 'long',
                'len_queue': len_queue
            }


@router.post("/upload", response_model=BaseResponse, )
async def add_check_file(file: UploadFile):
    """
        Додає файл в чергу на обробку
    """
    task = task_manager.delay(file.filename)
    return JSONResponse(create_response(
        message='Added file on processing',
        data={"task_id": task.id},
    ), status_code=status.HTTP_202_ACCEPTED)


@router.get("/status/{task_id}", response_model=BaseResponse)
async def get_status_or_result(task_id: str, page: list | None = None):
    """
        Перевірити статус, або отримати результат обробки файла
    """

    task = task_manager.AsyncResult(task_id)
    celery_manager = celery_app.control.inspect()

    data = {}
    message = "Get result or status task"

    data.update({
        'status': task.state,
        'id': task.id,
        'queue': None,
        'result': None
    })
    status_code = status.HTTP_200_OK
    new_add_tasks: dict = celery_manager.active()  # очікують, поки worker додасть в чергу на виконання
    tasks_in_queue: dict = celery_manager.reserved()  # додані worker задачі на обробку. Будуть оброблені раніше
    match task.state:
        case "PENDING":
            message = "Task in processing"
            queue_celery_info = GetCeleryTasks(task_id).get_detail_task_in_queue(
                list(tasks_in_queue.values())[0],
                list(new_add_tasks.values())[0],
            )
            data['queue'] = queue_celery_info
            status_code = status.HTTP_102_PROCESSING
        case "SUCCESS":
            message = "The task is completed"
            data['result'] = {}

        case "FAILURE":
            message = "The task was not completed successfully. Try again later send new file"
            status_code = status.HTTP_502_BAD_GATEWAY

    return JSONResponse(create_response(message=message, data=data), status_code=status_code)

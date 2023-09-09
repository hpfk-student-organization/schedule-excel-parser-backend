from fastapi import APIRouter, UploadFile, Form

from app.utils.celery_worker.main import task_manager

router = APIRouter()


@router.post("/upload")
async def add_check_file(file: UploadFile):
    task = task_manager.delay(file.filename)
    return {"task": task.id}


@router.get("/status/{task_id}")
async def get_status_or_result(task_id: str, page: list | None = None):
    task = task_manager.AsyncResult(task_id)

    return {"status": task.state}

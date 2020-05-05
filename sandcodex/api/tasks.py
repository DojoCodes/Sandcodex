from sandcodex.backend.app import get_result
from celery.result import AsyncResult

def get_tasks(task_id):
    task = AsyncResult(task_id)
    ret =  {
        "id": task.id,
        "status": task.state,
        "interpreter": "python",
        "code": "",
        "parameters": [],
        "results": [] if task.state != "SUCCESS" else task.result
    }
    return ret, 200

def post_tasks(body):
    task = get_result.delay(body['code'], body['parameters'])
    return {
        "id": task.id,
        "status": task.state,
        "interpreter": "python",
        "code": body['code'],
        "parameters": body['parameters'],
        "results": task.result if task.result is not None else []
    }, 202
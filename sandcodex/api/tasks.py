from sandcodex.backend.app import get_result
from celery.result import AsyncResult

def get_tasks(task_id):
    task = AsyncResult(task_id)
    result = task.result
    if result is None:
        result = []
    if isinstance(result, Exception):
        return {
            "message": f"There is an error in Job execution (task_id={task.id})",
            "status": 500,
            "title": "Internal Error",
            "type": result.__class__.__qualname__
        }
    return result, 200

def post_tasks(body):
    task = get_result.delay(
        interpreter=body.get('interpreter'),
        code=body.get('code'),
        parameters=body.get('parameters'),
        callback=body.get('callback', None))
    return {
        "id": task.id,
        "status": task.state,
        "interpreter": "python",
        "code": body['code'],
        "parameters": body['parameters'],
        "results": []
    }, 202
from sandcodex.backend.app import get_result
from celery.result import AsyncResult
from sandcodex.backend.config import interpreters


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
    if body.get('interpreter') not in interpreters.keys():
        return {
            "message": f"The interpreter '{body.get('interpreter')}' doesn't exist",
            "status": 400,
            "title": "Bad Request",
            "type": "InterpreterNotFoundError"
        }
    task = get_result.delay(
        interpreter=body.get('interpreter'),
        code=body.get('code'),
        inputs=body.get("inputs", []),
        callback=body.get('callback', None),
        attachments=body.get("attachments", {}))
    return {
        "id": task.id,
        "status": task.state,
        "interpreter": body.get('interpreter'),
        "code": body['code'],
        "inputs": body.get("inputs", []),
        "results": []
    }, 202

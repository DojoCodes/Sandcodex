from celery.exceptions import Ignore, SoftTimeLimitExceeded
from sandcodex.backend.utils import text_to_tar_stream 
from sandcodex.backend.worker import Worker
from sandcodex.backend.config import interpreters
from typing import List
from celery.utils.log import get_task_logger
from celery import Celery
import docker
import requests

logger = get_task_logger(__name__)

celery = Celery("sandcodex")

docker_client = docker.from_env()
workers = {
    name : Worker(
        client=docker_client,
        image=data["image"],
        command=data["command"],
    )
    for name, data in interpreters.items()
}

def update_status(task, state, result, callback):
    result["status"] = state
    if state != "SUCCESS":
        task.update_state(state=state, meta=result)
    if callback != None:
        requests.post(callback["url"], json=result, headers={"Authorization": f"Bearer {callback['bearer']}"})


@celery.task(bind=True, soft_time_limit=10, time_limit=15)
def get_result(self, interpreter: str, code: str, parameters: List[List[str]], callback: dict):
    container = None
    result = {
        "id": self.request.id,
        "status": "",
        "interpreter": interpreter,
        "code": code,
        "parameters": parameters,
        "results": None
    }
    try:
        update_status(self, state="STARTED", result=result, callback=callback)
        if interpreter not in workers:
            result["results"] = [f"Interpreter '{interpreter}' not found"]
            update_status(self, state="FAILURE", result=result, callback=callback)
            raise Ignore()
        worker = workers[interpreter]
        container = worker.new_container()
        results = []
        for parameter in parameters:
            results.append(container.exec(code, parameter))
        result["results"] = results
        update_status(self, state="SUCCESS", result=result, callback=callback)
        return result
    except SoftTimeLimitExceeded:
        update_status(self, state="TIMEOUT", result=result, callback=callback)
        raise Ignore()
    except:
        update_status(self, state="FAILURE", result=result, callback=callback)
        raise Ignore()
    finally:
        if hasattr(container, "up"):
            if container.up:
                container.kill()

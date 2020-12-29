from celery.exceptions import Terminated, SoftTimeLimitExceeded
from sandcodex.backend.utils import text_to_tar_stream
from sandcodex.backend.worker import Worker
from sandcodex.backend.config import interpreters
from typing import List, Dict, Any
from celery.utils.log import get_task_logger
from celery import Celery
import docker
import requests
import time


logger = get_task_logger(__name__)

celery = Celery("sandcodex")


workers = {
    name: Worker(
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
        requests.post(
            callback["url"],
            json=result,
            headers={"Authorization": f"Bearer {callback['bearer']}"},
        )


@celery.task(bind=True, soft_time_limit=10, time_limit=15)
def get_result(
    self,
    interpreter: str,
    code: str,
    inputs: List[Dict[str, Any]],
    callback: dict,
    attachments: Dict[str, str],
):
    container = None
    result = {
        "id": self.request.id,
        "status": "",
        "interpreter": interpreter,
        "code": code,
        "inputs": inputs,
        "results": None,
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
        for input_ in inputs:
            before_time = time.time()
            output = container.exec(
                code, input_.get("parameters", []), input_.get("stdin", ""), attachments
            )
            delta_time = time.time() - before_time
            results.append(
                {
                    "output": output,
                    "id": input_.get("id", ""),
                    "executionTime": round(delta_time, 4),
                }
            )
        result["results"] = results
        update_status(self, state="SUCCESS", result=result, callback=callback)
        return result
    except SoftTimeLimitExceeded as e:
        update_status(self, state="TIMEOUT", result=result, callback=callback)
        raise SoftTimeLimitExceeded(str(e)) from e
    except:
        update_status(self, state="FAILURE", result=result, callback=callback)
        raise Terminated()
    finally:
        if hasattr(container, "up"):
            if container.up:
                container.kill()

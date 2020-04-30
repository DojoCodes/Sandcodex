from celery import Celery
from celery.exceptions import Ignore, SoftTimeLimitExceeded
from sandcodex.utils import text_to_tar_stream 
from sandcodex.docker import Worker
from typing import List
import docker

celery = Celery("sandcodex")
docker_client = docker.from_env()
python_worker = Worker(
    client=docker_client,
    image="sandcodex_worker_python:latest",
    command="python code.py {parameters}",
)


@celery.task(bind=True, soft_time_limit=10, time_limit=15)
def get_result(self, code: str, parameters: List[str]):
    self.update_state(state='STARTED')
    container = None
    try:
        container = python_worker.new_container()
        result = []
        for parameter in parameters:
            result.append(container.exec(code, parameter))
        return result
    except SoftTimeLimitExceeded:
        self.update_state(state='TIMEOUT')
        raise Ignore()
    except:
        self.update_state(state='FAILURE')
        raise Ignore()
    finally:
        if hasattr(container, "up"):
            if container.up:
                container.kill()

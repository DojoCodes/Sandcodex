import docker
from sandcodex.utils import text_to_tar_stream

class Worker:
    
    def __init__(self, client: docker.client.DockerClient, image: str, command: str):
        self.client = client
        self.image = image
        self.command = command

    def new_container(self):
        return Container(self.client, self.image, self.command)

class Container:
    
    def __init__(self, client: docker.client.DockerClient, image: str, command: str):
        self.client = client
        self.image = image
        self.command = command
        self.container = self.client.containers.run(
            image=self.image, detach=True, network_mode="none"
        )
    
    def exec(self, code, parameters):
        command = self.command.format(
            parameters=" ".join(parameters)
        )
        tar_stream = text_to_tar_stream(code, name="code.py")
        self.container.put_archive(
            path=f"/home/worker", data=tar_stream
        )
        return_code, stream = self.container.exec_run(command, stream=True)
        ret = ""
        for line in stream:
            if isinstance(line, bytes):
                ret += line.decode()
        return ret

    @property
    def up(self):
        if not self.container:
            return False
        return self.container.status == "created" or self.container.status == "running"

    def kill(self):
        self.container.kill()
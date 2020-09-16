import docker
from sandcodex.backend.utils import text_to_tar_stream


class Worker:

    def __init__(self, image: str, command: str, client: docker.client.DockerClient = None):
        self._client = client
        self.image = image
        self.command = command

    def new_container(self):
        return Container(self.client, self.image, self.command)

    @property
    def client(self):
        if not self._client:
            self._client = docker.from_env()
        return self._client


class Container:

    def __init__(self, client: docker.client.DockerClient, image: str, command: str):
        self.client = client
        self.image = image
        self.command = command
        self.container = self.client.containers.run(
            image=self.image, detach=True, network_mode="none", stdin_open=True
        )

    def exec(self, code, parameters, input_):
        command = self.command.format(
            parameters=" ".join(parameters)
        )
        tar_stream = text_to_tar_stream(code, name="code.py")
        self.container.put_archive(
            path=f"/home/worker", data=tar_stream
        )
        _, stream = self.container.exec_run(command, socket=True, stdin=True, stdout=True, stderr=True)
        ret = ""
        stream._sock.send(input_.encode('utf8'))
        while True:
            data = stream._sock.recv(1024)
            if not data: break
            ret += data[8:].decode('utf8')
        return ret

    @property
    def up(self):
        if not self.container:
            return False
        return self.container.status == "created" or self.container.status == "running"

    def kill(self):
        self.container.kill()
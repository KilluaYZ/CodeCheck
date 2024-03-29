import docker
from codecheck.database.Mongo import Mongo

mongo = Mongo()

class DockerImage:
    def __init__(self, image_name: str, image_version: str='latest'):
        self.image_name = image_name
        self.image_version = image_version

class DockerContainer:
    def __init__(self):
        self.status = 'stop'
        self.container_id = None
        self.ws_host = None
        self.ws_port = None
        self.ssh_host = None
        self.ssh_port = None
        self.share_dir = None

    def connect(self):
        if self.container_id is None:
            raise Exception('container_id is None')
        self.client = docker.from_env().containers.get(self.container_id)
        if self.client.status != 'running':
            self.client.start()

    def execute(self, command: str):
        if self.client is None:
            self.connect()
        self.client.exec_run(command)

class DockerManager:
    def __init__(self):

    def get_container_by_project_id(self):
        pass

    def get_container_by_container_id(self, container_id: str) -> DockerContainer:
        row = mongo.find_one('Container', {"container_id": container_id})
        if row is None:
            return None
        container = DockerContainer()
        container.container_id = row['container_id']
        container.ws_host = row['container_id']
        container.ws_port = row['container_id']
        container.ssh_host = row['container_id']
        container.ssh_port = row['container_id']
        container.share_dir = row['container_id']
        return container

    def run_container(self, image: DockerImage):
        pass

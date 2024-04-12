import docker
import socket
from codecheck.database.Mongo import Mongo
import random
import datetime
import config
import os
import shutil
import threading

mongo = Mongo()


def exec_cmd_thread(client, cmd):
    client.exec_run(cmd)

class DockerContainer:
    def __init__(self):
        self.status = 'stop'
        self.container_id = None
        self.ws_host = None
        self.ws_port = None
        self.ssh_host = None
        self.ssh_port = None
        self.share_dir = None
        self.client = None
        self.name = None
        self.create_time = None

    def get_client(self):
        if self.container_id is None:
            raise Exception('container_id is None')
        if self.client is None:
            self.client = docker.from_env().containers.get(self.container_id)
        return self.client

    def start(self):
        client = self.get_client()
        if client.status != 'running':
            client.start()
            self.execute_async("nohup node /root/ws_server/index.js &")
            self.execute_async("service ssh start")
        self.update_status()

    def execute_async(self, cmd):
        client = self.get_client()
        threading.Thread(target=exec_cmd_thread, args=(client,cmd)).start()

    def stop(self):
        client = self.get_client()
        client.stop()
        self.update_status()

    def remove(self):
        client = self.get_client()
        client.remove()
        self.release_container()

    def get_ws_host(self) -> tuple:
        if self.ws_host is None or self.ws_port is None:
            raise Exception('ws_host or ws_port is None')
        return self.ws_host, self.ws_port

    def get_ssh_host(self) -> tuple:
        if self.ssh_host is None or self.ssh_port is None:
            raise Exception('ssh_host or ssh_port is None')
        return self.ssh_host, self.ssh_port

    def update_status(self):
        client = self.get_client()
        self.status = client.status
        mongo.update_one('Container', {"container_id": self.container_id}, {"$set": {"status": self.status}})

    # 删除容器占用的全部资源
    def release_container(self):
        shutil.rmtree(self.share_dir)
        mongo.delete_one('Container', {"container_id": self.container_id})

    def execute(self, command: str):
        if self.client is None:
            self.start()
        self.client.exec_run(command)

    def from_dict(self, data: dict):
        if 'ssh_host' in data:
            self.ssh_host = data['ssh_host']
        if 'ssh_port' in data:
            self.ssh_port = data['ssh_port']
        if 'ws_host' in data:
            self.ws_host = data['ws_host']
        if 'ws_port' in data:
            self.ws_port = data['ws_port']
        if 'share_dir' in data:
            self.share_dir = data['share_dir']
        if 'container_id' in data:
            self.container_id = data['container_id']
        if 'status' in data:
            self.status = data['status']
        if 'name' in data:
            self.name = data['name']

    def to_dict(self) -> dict:
        return {
            "ssh_host": self.ssh_host,
            "ssh_port": self.ssh_port,
            "ws_host": self.ws_host,
            "ws_port": self.ws_port,
            "share_dir": self.share_dir,
            "container_id": self.container_id,
            "status": self.status,
            "name": self.name,
            "create_time": self.create_time
        }

class DockerManager:
    def __init__(self, host='127.0.0.1', share_dir=config.SHARE_DIR, container_img=config.DOCKER_IMAGE):
        self.host = host
        self.client = docker.from_env()
        self.share_dir = share_dir
        self.container_img = container_img

    def get_container(self, container_id: str) -> DockerContainer:
        row = mongo.find_one('Container', {"container_id": container_id})
        if row is None:
            return None
        container = DockerContainer()
        container.container_id = row['container_id']
        container.ws_host = row['ws_host']
        container.ws_port = row['ws_port']
        container.ssh_host = row['ssh_host']
        container.ssh_port = row['ssh_port']
        container.share_dir = row['share_dir']
        return container

    def run_container(self, name: str) -> DockerContainer:
        # 先获取所有docker容器的端口占用情况
        host_ports = self.get_available_ports()
        container = DockerContainer()
        container.from_dict(host_ports)
        container.name = name
        container.create_time = datetime.datetime.now()
        row = mongo.insert_one("Container", container.to_dict())
        _id = row.inserted_id
        container.share_dir = f"{self.share_dir}/{str(_id)}"
        mongo.update_one("Container", {"_id": _id}, {"$set":{"share_dir": container.share_dir}})
        os.makedirs(container.share_dir, exist_ok=True)
        container_obj = self.client.containers.run(
            image=self.container_img,
            ports={f'22/tcp':container.ssh_port, f'8898/tcp': container.ws_port},
            volumes=[f'{container.share_dir}:/share'],
            detach=True,
            init=True,
            tty=True
        )
        container.container_id = container_obj.id
        mongo.update_one("Container", {"_id": _id}, {"$set":{"container_id": container.container_id}})
        container.update_status()
        container.start()
        return container

    def list_container(self) -> list:
        return list(mongo.find("Container"))

    # 获取可用的ssh和ws的映射端口
    def get_available_ports(self) -> dict:
        ws_host = self.host
        ssh_host = self.host
        ssh_port = -1
        ws_port = -1
        try_cnt = 0
        while(try_cnt < 100):
            try_cnt += 1
            ssh_port = int(random.randint(10000,65535))
            if not self.is_port_in_use(ssh_port):
                break
        if try_cnt >= 100:
            raise Exception("随机分配ssh端口失败")
        try_cnt = 0
        print("finish ssh")
        while (try_cnt < 100):
            try_cnt += 1
            ws_port = int(random.randint(10000, 65535))
            if not self.is_port_in_use(ws_port):
                break
        if try_cnt >= 100:
            raise Exception("随机分配ws端口失败")

        return {
            "ssh_host": ssh_host,
            "ssh_port": ssh_port,
            "ws_host": ws_host,
            "ws_port": ws_port
        }

    def is_port_in_use(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
            except:
                return True

        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
            try:
                s.bind(('::', port))
            except:
                return True

        return False

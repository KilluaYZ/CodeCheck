import docker
for c in docker.from_env().containers.list():
    print(f"id = {c.id}")
    print(f"image = {c.image}")
    print(f"labels = {c.labels}")
    print(f"name = {c.name}")
    print(f"short_id = {c.short_id}")
    print(f"status = {c.status}")
    print(f"id = {c.id}")

print()
print()

for n in docker.from_env().networks.list():
    print(f"id = {n.id}")
    print(f"short_id = {n.short_id}")
    print(f"name = {n.name}")
    print(f"containers = {n.containers}")


import socket
def is_port_in_use(port) -> bool:
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

print(is_port_in_use(80))

for i in range(0, 65535):
    if is_port_in_use(i):
        print(f"{i} is in use")

import paramiko
import time
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='127.0.0.1', port=10022, username='root', password='123456')
channel = ssh.invoke_shell()
time.sleep(2)
output = channel.recv(2048)
print(output.decode(), end='')
while(True):
    cmd = input()
    channel.send(cmd + '\n')
    output = channel.recv(2048)
    print(output.decode(), end='')
import paramiko
import pandas as pd

# Пример использования:

hostname = '31.129.102.161'
username = 'root'
password = 'S123q456!'

def make_docker_df(info: str):
    text = re.sub(r'\s+', ' ', docker_info.split("\n")[0]).strip().split(' ')
    r = {}
    r[' '.join(text[:2])] = []
    for i in text[2:]:
        r[i] = []


    q = []
    for i in docker_info.split("\n")[1:]:
        t = []
        for x in i.split("   "):
            if x:
                t.append(x)
        q.append(t)

    x = 0
    for k in r.keys():
        for i in q:
            try:
                if k == "PORTS" and not isinstance(i, int):
                    r["NAMES"].append(i[x])
                    r[k].append(None)
                else:
                    r[k].append(i[x])
            except:
                pass
        x += 1

    return pd.DataFrame(r)

def get_linux_distribution(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command('cat /etc/os-release')
        os_info = stdout.read().decode('utf-8')
        return os_info
    except Exception as e:
        print(f"Error connecting to the server: {e}")
    finally:
        client.close()

def ssh_command(hostname, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        return output
    except Exception as e:
        print(f"Error connecting to the server: {e}")
    finally:
        client.close()


def get_running_vm_info(hostname, username, password):
    command = 'virsh list --all'
    return ssh_command(hostname, username, password, command)


def get_docker_containers(hostname, username, password):
    command = 'docker ps -a'
    docker_info = ssh_command(hostname, username, password, command)
    return make_docker_df(docker_info)


def stop_docker_container(hostname, username, password, container_id):
    command = f'docker stop {container_id}'
    return ssh_command(hostname, username, password, command)


def run_docker_container(hostname, username, password, container_id):
    command = f'docker container start {container_id}'
    return ssh_command(hostname, username, password, command)


def stop_virtual_machine(hostname, username, password, vm_name):
    command = f'virsh destroy {vm_name}'
    return ssh_command(hostname, username, password, command)

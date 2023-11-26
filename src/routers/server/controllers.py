from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import Server
from src.schemas import ServerCreate
from src.routers.auth.controllers import get_one_user
import re
import pandas as pd
import paramiko


def make_docker_df(info: str):
    text = re.sub(r'\s+', ' ', info.split("\n")[0]).strip().split(' ')
    r = {}
    r['_'.join(text[:2])] = []
    for i in text[2:]:
        r[i] = []

    q = []
    for i in info.split("\n")[1:]:
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


def make_vm_data_windows(t):
    x = {}
    for i in t.replace('-', '').split('\n')[0].split(" "):
        if i:
            x[i] = []

    n = []
    for i in t.replace('-', '').split('\n')[2:]:
        nn = []
        p = i.split(" ")
        for q in p:
            if q:
                nn.append(q)
        n.append(nn)

    y = 0
    for k in x.keys():
        for i in n:
            x[k].append(i[y])
        y += 1

    df = pd.DataFrame(x)
    df['status'] = df['State'].apply(lambda x: 0 if str(x) == "Off" else 1)
    return df


def make_vm_data_liunx(t):
    x = {}
    for i in t.replace('-', '').split('\n')[0].split(" "):
        if i:
            x[i] = []

    n = []
    for i in t.split('\n')[2:]:
        nn = []
        p = i.split(" ")
        for q in p:
            if q:
                nn.append(q)
        n.append(nn)

    y = 0
    for k in x.keys():
        for i in n:
            x[k].append(i[y])
        y += 1

    df = pd.DataFrame(x)
    df['status'] = df['State'].apply(lambda x: 1 if str(x).startswith("run") else 0)
    return df


def compile_data(info: str):
    df = make_docker_df(info)
    df['status'] = df['STATUS'].apply(lambda x: 1 if str(x).startswith("Up") else 0)
    return df.values.tolist()

async def get_servers(db: AsyncSession, skip: int = 0, limit: int = 100):
    q = select(Server).offset(skip).limit(limit)
    servers = await db.execute(q)
    return servers.scalars().all()


async def get_one_server(db: AsyncSession, servername: str):
    q = select(Server).where(Server.name == servername)
    server = await db.execute(q)
    return server.scalars().first()


async def get_all_user_server(db: AsyncSession, id: int):
    q = select(Server).where(Server.owner_id == id)
    server = await db.execute(q)
    return server.scalars().fetchall()


async def create_user_server(db: AsyncSession, server: ServerCreate, login: str):
    user = await get_one_user(db, login)
    try:
        db_item = Server(**server.dict(), owner_id=user.id)
    except:
        return None
    db.add(db_item)
    await db.commit()
    return db_item


def ssh_command_linux(hostname, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        for comm in command:
            stdin, stdout, stderr = client.exec_command(comm)
            output = stdout.read().decode('utf-8')
        return output
    except Exception as e:
        print(f"Error connecting to the server: {e}")
    finally:
        client.close()

def ssh_command_windows(hostname, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        for comm in command:
            stdin, stdout, stderr = client.exec_command(f'powershell -Command "{comm}"')
            output = stdout.read().decode('latin-1')
        return output
    except Exception as e:
        print(f"Error connecting to the server: {e}")
    finally:
        client.close()


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

def get_running_vm_info_linux(hostname, username, password):
    command = ['source /etc/profile && virsh list --all']
    output = ssh_command_linux(hostname, username, password, command)
    return make_vm_data_liunx(output)


def get_running_vm_info_windows(hostname, username, password):
    command = ['Get-VM']
    output = ssh_command_windows(hostname, username, password, command)
    return make_vm_data_windows(output)

def stop_virtual_machine_linux(hostname, username, password, vm_name):
    command = [f'source /etc/profile && virsh destroy {vm_name}']
    return ssh_command_linux(hostname, username, password, command)


def start_virtual_machine_linux(hostname, username, password, vm_name):
    command = [f'source /etc/profile && virsh start {vm_name}']
    return ssh_command_linux(hostname, username, password, command)


def start_virtual_machine_windows(hostname, username, password, vm_name):
    command = [f'Start-VM -Name "{vm_name}"']
    return ssh_command_windows(hostname, username, password, command)


def stop_virtual_machine_windows(hostname, username, password, vm_name):
    command = [f'Stop-VM -Name "{vm_name}" -Force']
    return ssh_command_windows(hostname, username, password, command)

def get_docker_containers(hostname, username, password):
    command = ['docker ps -a']
    if get_linux_distribution(hostname, username, password):
        docker_info = ssh_command_linux(hostname, username, password, command)
    else:
        docker_info = ssh_command_windows(hostname, username, password, command)
    return compile_data(docker_info)


def stop_docker_container(hostname, username, password, container_id):
    command = [f'docker stop {container_id}']
    if get_linux_distribution(hostname, username, password):
        docker_info = ssh_command_linux(hostname, username, password, command)
    else:
        docker_info = ssh_command_windows(hostname, username, password, command)
    return docker_info


def start_docker_container(hostname, username, password, container_id):
    command = [f'docker start {container_id}']
    if get_linux_distribution(hostname, username, password):
        docker_info = ssh_command_linux(hostname, username, password, command)
    else:
        docker_info = ssh_command_windows(hostname, username, password, command)
    return docker_info


def run_docker_container(hostname, username, password, container_name, img):
    command = [f'docker run --name {container_name} -d {img}']
    if get_linux_distribution(hostname, username, password):
        docker_info = ssh_command_linux(hostname, username, password, command)
    else:
        docker_info = ssh_command_windows(hostname, username, password, command)
    return docker_info


def remove_docker_container(hostname, username, password, container):
    command = [f'docker stop {container}', f'docker remove {container}']
    if get_linux_distribution(hostname, username, password):
        docker_info = ssh_command_linux(hostname, username, password, command)
    else:
        docker_info = ssh_command_windows(hostname, username, password, command)
    return docker_info


def pull_docker_container(hostname, username, password, name):
    command = [f'docker pull {name}']
    if get_linux_distribution(hostname, username, password):
        docker_info = ssh_command_linux(hostname, username, password, command)
    else:
        docker_info = ssh_command_windows(hostname, username, password, command)
    return docker_info

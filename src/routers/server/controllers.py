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
    r[' '.join(text[:2])] = []
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

async def get_servers(db: AsyncSession, skip: int = 0, limit: int = 100):
    q = select(Server).offset(skip).limit(limit)
    servers = await db.execute(q)
    return servers.scalars().all()

async def get_one_server(db: AsyncSession, servername: str):
    q = select(Server).where(Server.name == servername)
    server = await db.execute(q)
    return server.scalars().first()


async def create_user_server(db: AsyncSession, server: ServerCreate, login: str):
    user = await get_one_user(db, login)
    try:
        db_item = Server(**server.dict(), owner_id=user.id)
    except:
        return None
    db.add(db_item)
    await db.commit()
    return db_item


def ssh_command(hostname, username, password, command):
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

def get_docker_containers(hostname, username, password):
    command = ['docker ps -a']
    docker_info = ssh_command(hostname, username, password, command)
    return make_docker_df(docker_info)

def stop_docker_container(hostname, username, password, container_id):
    command = [f'docker stop {container_id}']
    return ssh_command(hostname, username, password, command)

def start_docker_container(hostname, username, password, container_id):
    command = [f'docker start {container_id}']
    return ssh_command(hostname, username, password, command)

def run_docker_container(hostname, username, password, container_name, img):
    command = [f'docker run --name {container_name} -d {img}']
    return ssh_command(hostname, username, password, command)

def remove_docker_container(hostname, username, password, container):
    command = [f'docker stop {container}', f'docker remove {container}']
    return ssh_command(hostname, username, password, command)

def pull_docker_container(hostname, username, password, name):
    command = [f'docker pull {name}']
    return ssh_command(hostname, username, password, command)

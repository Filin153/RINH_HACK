import paramiko

# Пример использования:

hostname = '31.129.102.161'
username = 'root'
password = 'S123q456!'


# def get_linux_distribution(hostname, username, password):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#     try:
#         client.connect(hostname, username=username, password=password)
#         stdin, stdout, stderr = client.exec_command('cat /etc/os-release')
#         os_info = stdout.read().decode('utf-8')
#         return os_info
#     except Exception as e:
#         print(f"Error connecting to the server: {e}")
#     finally:
#         client.close()
#
#
# linux_distribution_info = get_linux_distribution(hostname, username, password)
#
# print(f"Linux Distribution Information:\n{linux_distribution_info}")


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


def get_running_docker_containers(hostname, username, password):
    command = 'docker ps -a'
    return ssh_command(hostname, username, password, command)


def stop_docker_container(hostname, username, password, container_id):
    command = f'docker stop {container_id}'
    return ssh_command(hostname, username, password, command)


def run_docker_container(hostname, username, password, container_id):
    command = f'docker container start {container_id}'
    return ssh_command(hostname, username, password, command)


def stop_virtual_machine(hostname, username, password, vm_name):
    command = f'virsh destroy {vm_name}'
    return ssh_command(hostname, username, password, command)


# # Получение информации о запущенных виртуальных машинах
# vm_info = get_running_vm_info(hostname, username, password)
# print("Running Virtual Machines:")
# print(vm_info)
container_id_to_stop = '6323a3cb3b5c'
run_docker_container(hostname, username, password, container_id_to_stop)
print(f"\nRun Docker Container: {container_id_to_stop}")

container_id_to_stop = '53cf8c403533'
stop_docker_container(hostname, username, password, container_id_to_stop)
print(f"\nStop Docker Container: {container_id_to_stop}")

# Получение информации о запущенных Docker контейнерах
docker_info = get_running_docker_containers(hostname, username, password)
print("\nRunning Docker Containers:")
print(docker_info)

# # Остановка виртуальной машины (замените 'vm_name' на реальное имя виртуальной машины)
# vm_name_to_stop = 'your_vm_name'
# stop_virtual_machine(hostname, username, password, vm_name_to_stop)
# print(f"\nStopped Virtual Machine: {vm_name_to_stop}")

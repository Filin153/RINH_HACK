import paramiko

hostname = 'ip_adress'
username = 'username'
password = 'password'


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


def ssh_command_linux(hostname, username, password, command):
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


def ssh_command_windows(hostname, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(f'powershell -Command "{command}"')
        output = stdout.read().decode('latin-1')
        return output
    except Exception as e:
        print(f"Error connecting to the server: {e}")
    finally:
        client.close()


def get_running_vm_info_linux(hostname, username, password):
    command = 'source /etc/profile && virsh list --all'
    output = ssh_command_linux(hostname, username, password, command)
    return output


def get_running_vm_info_windows(hostname, username, password):
    command = 'Get-VM'
    output = ssh_command_windows(hostname, username, password, command)
    return output


def get_running_docker_containers(hostname, username, password):
    command = 'docker ps -a'
    return ssh_command_linux(hostname, username, password, command)


def stop_docker_container(hostname, username, password, container_id):
    command = f'docker stop {container_id}'
    return ssh_command_linux(hostname, username, password, command)


def run_docker_container(hostname, username, password, container_id):
    command = f'docker container start {container_id}'
    return ssh_command_linux(hostname, username, password, command)


def stop_virtual_machine_linux(hostname, username, password, vm_name):
    command = f'source /etc/profile && virsh destroy {vm_name}'
    return ssh_command_linux(hostname, username, password, command)


def start_virtual_machine_linux(hostname, username, password, vm_name):
    command = f'source /etc/profile && virsh start {vm_name}'
    return ssh_command_linux(hostname, username, password, command)


def start_virtual_machine_windows(hostname, username, password, vm_name):
    command = f'Start-VM -Name "{vm_name}"'
    return ssh_command_windows(hostname, username, password, command)


def stop_virtual_machine_windows(hostname, username, password, vm_name):
    command = f'Stop-VM -Name "{vm_name}" -Force'
    return ssh_command_windows(hostname, username, password, command)

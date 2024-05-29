import paramiko
import os
import shutil

def create_ssh_client(server, port, user, key_filepath):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, key_filename=key_filepath)
    return client

def scp_transfer(ssh_client, local_path, remote_path):
    sftp = ssh_client.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()

def create_zip(local_path, zip_name):
    shutil.make_archive(zip_name, 'zip', local_path)
    return f"{zip_name}.zip"

def main():
    server = '54.144.129.122'         # IP o nombre de la máquina remota
    port = 22                         # Puerto SSH, generalmente es el 22
    user = 'ubuntu'                   # Usuario para la conexión SSH
    key_filepath = '/home/ubuntu/.ssh/id_rsa'  # Ruta a la clave privada

    local_path = '/home/ubuntu/proyectosNode/'  # Ruta local del archivo o directorio a respaldar
    zip_name = '/home/ubuntu/proyectosNode_backup'  # Nombre del archivo zip sin la extensión
    remote_path = '/tmp/backup/proyectosNode_backup.zip'  # Ruta remota donde se almacenará el respaldo

    # Crear el archivo zip
    zip_file = create_zip(local_path, zip_name)

    # Crear la conexión SSH y transferir el archivo zip
    ssh_client = create_ssh_client(server, port, user, key_filepath)
    scp_transfer(ssh_client, zip_file, remote_path)
    ssh_client.close()

    # Eliminar el archivo zip local después de la transferencia (opcional)
    os.remove(zip_file)

if __name__ == '__main__':
    main()

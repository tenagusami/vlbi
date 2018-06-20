import paramiko as pa
import my_settings as my


def ssh_setting():
    return my.vlbi_host()


def get_command_output(command):
    host_setting = ssh_setting()
    with pa.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(pa.AutoAddPolicy())
        ssh.connect(
            hostname=host_setting.ip_address,
            port=22,
            username=host_setting.username,
            password=host_setting.password)
        stdin, stdout, stderr = ssh.exec_command(command)
        return [f.split("\n")[0] for f in stdout]


def get_files(remote_dir, local_dir,
              path_predicate=lambda x: True):
    host_setting = ssh_setting()
    with pa.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(pa.AutoAddPolicy())
        ssh.connect(
            hostname=host_setting['IP address'],
            port=22,
            username=host_setting['username'],
            password=host_setting['password'])
        with ssh.open_sftp() as sftp:
            try:
                sftp.chdir(remote_dir)
            except IOError:
                raise RuntimeError(
                    'the specified directory ' + remote_dir + 'does not exist.')
            remote_file_names \
                = [file_name for file_name in sftp.listdir()
                   if path_predicate(file_name)]
            local_file_paths = [local_dir + '/' + file_name
                                for file_name in remote_file_names]
            remote_file_stat = []
            for remote_file_name, local_file_path \
                    in zip(remote_file_names, local_file_paths):
                try:
                    sftp.get(remote_file_name, local_file_path)
                    file_stat = sftp.stat(remote_file_name)
                except:
                    raise RuntimeError(
                        'failure to fetch the file ' + remote_dir +
                        '/' + remote_file_name + ' from operation.')
                remote_file_stat.append(file_stat)
            return list(zip(local_file_paths, remote_file_stat))

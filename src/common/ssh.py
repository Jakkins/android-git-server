import os
import platform
import re
import subprocess
from src.common.utils import read_file_content
from src.logg import logg
from src.termux.termux_utils import run_command_in_termux

HOME = os.path.expanduser("~")
_platform = platform.system()
SSH_COMMAND = "ssh.exe" if _platform == "Windows" else "ssh"
PRIVK = os.path.join(HOME, ".ssh", "ags-key")
PUBK = os.path.join(HOME, ".ssh", "ags-key.pub")

def are_keys_present():
    logg().info(f"checking keys presence in {HOME}")
    if not os.path.exists(PRIVK):
        logg().warning("private key not found.")
    if not os.path.exists(PUBK):
        logg().warning("public key not found.")
    return os.path.exists(PRIVK) and os.path.exists(PUBK)


def create_ssh_key_pair():
    user_ssh_dir = os.path.join(HOME, ".ssh")
    if not os.path.exists(user_ssh_dir):
        os.makedirs(user_ssh_dir)
    if (os.path.exists(PRIVK) and os.path.exists(PUBK)):
        logg().info("key pair already exists")
        return
    try:
        os.remove(PRIVK)
    except:
        pass
    try:
        os.remove(PUBK)
    except:
        pass
    logg().info("creating key pairs")
    os.system(f'cd {user_ssh_dir} && ssh-keygen -o -t ed25519 -C "ags" -f "ags-key" -N "''"')


def create_ssh_configuration():
    """
    Will check if the configuration is already present.
    Will work only in localhost mode.
    """
    logg().info("checking ssh configuration")
    with open(f"{HOME}/.ssh/config", "a+", encoding="utf-8") as f:
        f.seek(0)
        config = f.read()
        line = re.findall('\\s(ags)\\s', config)
        if not line:
            f.writelines(
                ["\n\nHost localhost", "\n  HostName localhost", "\n  User ags", f"\n  IdentityFile {HOME}/.ssh/ags-key"])

def get_pub_key():
    return read_file_content(f"{HOME}/.ssh/ags-key.pub", "UTF-8")


def export_pub_key_in_termux_sshd():
    # check if pubk already present in authorized_keys
    pubk = get_pub_key()
    pubk = pubk.replace('\n', '').replace('\r', '')
    run_command_in_termux("mkdir -p /data/data/com.termux/files/home/.ssh/")
    run_command_in_termux("bash")
    pubk_key_str = pubk.split(" ")[1]
    run_command_in_termux(f'result=\\$\\(grep -oe {pubk_key_str} /data/data/com.termux/files/home/.ssh/authorized_keys\\)\\;')
    # in windows this work -> $result 
    command = f"""
    if \\[ -z '$result' \\]\\; then echo {pubk} \\>\\> /data/data/com.termux/files/home/.ssh/authorized_keys\\; else echo key already added\\; fi
	""".strip().replace("\n", "")
    run_command_in_termux(command)
    run_command_in_termux("cat /data/data/com.termux/files/home/.ssh/authorized_keys")

def run_command_with_ssh(command_string: str):
    # todo check if first connection === Are you sure you want to continue connecting (yes/no/[fingerprint])?
    privk = os.path.join(HOME, ".ssh", "ags-key")
    command = f"{SSH_COMMAND} -i {privk} -p 8022 localhost {command_string}"
    shell = True if platform.system() == "Windows" else False
    result = subprocess.run(command.split(
        " "), shell=shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8", check=False)
    if result.returncode != 0:
        logg().error(result.stderr)
        logg().warning("try to run this command to see why it's failing: ")
        logg().warning(f"{command}")
        return ""
    return result.stdout